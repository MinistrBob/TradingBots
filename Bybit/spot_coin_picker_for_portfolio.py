from pybit.unified_trading import HTTP
import json
import sqlite3
import traceback
from sqlite_db import create_database, update_date_last_check
from utils import unixtime_to_datetime, get_current_unixtime
from datetime import datetime, timezone


def main():
    try:
        bybit_api = HTTP(
            testnet=False,
            api_key=r"RFnhyD7SwLfxnrUHwf",
            api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
        )
        conn_db = create_database()

        # get_tickers(bybit_api, conn_db, 'BTCUSDT')
        # exit()

        # symbols_list = get_symbols_list(bybit_api)
        # TODO: Здесь нужно реализовать цикл по всем монетам.
        get_kline_history(bybit_api, conn_db, 'BTCUSDT')
        get_tickers(bybit_api, conn_db, 'BTCUSDT')
        symbol_data_processing(conn_db, 'BTCUSDT')
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if 'conn_db' in locals() and conn_db is not None:
            try:
                conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)

def get_symbols_list(bybit_api):
    symbols = bybit_api.get_instruments_info(category='spot')
    print(json.dumps(symbols, indent=4))
    # file_path = r'c:\MyGit\TradingBots\Bybit\spot_symbols.json'
    # with open(file_path, 'r', encoding='utf-8') as f:
    #     symbols = json.load(f)
    # print(symbols)
    print(len(symbols["result"]["list"]))
    # Extract all symbols where quoteCoin is USDT
    usdt_symbols = [item["symbol"] for item in symbols["result"]["list"] if item["quoteCoin"] == "USDT"]
    # Sort the list of symbols alphabetically
    usdt_symbols_sorted = sorted(usdt_symbols)
    # Print the filtered symbols
    print(len(usdt_symbols_sorted), usdt_symbols_sorted)

    return usdt_symbols_sorted


def batch_insert_klines_to_db(conn_db, klines):
    """
    Вставляет несколько свечей в базу данных в одной операции.
    Если запись с таким startTime уже существует, обновляет данные.
    """
    cursor = conn_db.cursor()
    try:
        # Подготовка данных для batch-вставки
        data_to_insert = [
            (
                int(kline[0]),  # startTime
                float(kline[1]),  # open
                float(kline[2]),  # high
                float(kline[3]),  # low
                float(kline[4]),  # close
                float(kline[5]),  # volume
                float(kline[6])  # turnover
            ) for kline in klines
        ]

        # Выполняем batch-вставку с обработкой конфликта
        cursor.executemany('''
        INSERT INTO kline_history ([startTime], [open], [high], [low], [close], [volume], [turnover])
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT([startTime]) DO UPDATE SET
            [open]=excluded.[open],
            [high]=excluded.[high],
            [low]=excluded.[low],
            [close]=excluded.[close],
            [volume]=excluded.[volume],
            [turnover]=excluded.[turnover]
        ''', data_to_insert)
        conn_db.commit()
    except sqlite3.Error as e:
        raise Exception(f"Error in batch_insert_klines_to_db: {e}") from e



def insert_kline_to_db(conn_db, kline):
    """
    Вставляет одну свечу в базу данных.
    """
    cursor = conn_db.cursor()
    try:
        cursor.execute('''
        INSERT INTO kline_history (startTime, open, high, low, close, volume, turnover)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(kline[0]),  # startTime
            float(kline[1]),  # open
            float(kline[2]),  # high
            float(kline[3]),  # low
            float(kline[4]),  # close
            float(kline[5]),  # volume
            float(kline[6])  # turnover
        ))
        conn_db.commit()
    except sqlite3.IntegrityError:
        # Если запись с таким startTime уже существует, ничего не делаем
        print(f"Запись с startTime {kline[0]} уже существует в базе данных.")


def get_kline_history(bybit_api, conn_db, symbol):
    """
    Получение истории свечей для торговой пары для 1D.
    Выборка происходит в обратном порядке от end к start (от сегодня в прошлое).
    """
    end_time = get_current_unixtime()
    start_time = 0
    limit = 1000
    interval_ms = 24 * 60 * 60 * 1000  # Интервал 1 день в миллисекундах
    date_last_check = 0
    while True:
        # Запрашиваем следующие 1000 свечей
        response = bybit_api.get_kline(
            category="spot",
            symbol=symbol,
            interval="D",
            limit=limit,
            start=start_time,
            end=end_time,
        )
        klines = response['result']['list']
        # Печатаем первую, вторую и последнюю свечу для контроля
        if klines:
            if date_last_check == 0:
                date_last_check = int(klines[0][0])
            print(f"{unixtime_to_datetime(int(klines[0][0]))}\n{klines[0]}")
            # print(f"{unixtime_to_datetime(int(klines[1][0]))}\n{klines[1]}")
            print("...")
            print(f"{unixtime_to_datetime(int(klines[-1][0]))}\n{klines[-1]}")
            # Вставляем свечи в базу данных одной batch-вставкой
            batch_insert_klines_to_db(conn_db, klines)
            # Вставляем каждую свечу в базу данных
            # for kline in klines:
            #     insert_kline_to_db(kline)
        else:
            # Если ничего не вернулось, выходим из функции
            print("klines is empty")
            return
        # Обновляем end_time для следующего запроса
        last_time = int(klines[-1][0])
        if len(klines) < 1000:
            break
        # Устанавливаем новое начальное время для следующей итерации
        end_time = last_time - interval_ms
        print("===========================")
    update_date_last_check(conn_db, symbol, date_last_check)

def get_tickers(bybit_api, conn_db, symbol):
    tickers = bybit_api.get_tickers(category="spot", symbol=symbol)
    print(tickers)
    last_price = tickers['result']['list'][0]['lastPrice']
    volume_usdt = int(float(tickers['result']['list'][0]['turnover24h']))
    print(last_price, volume_usdt)
    cursor = None
    if last_price is not None and volume_usdt is not None:
        cursor = conn_db.cursor()
        # Обновляем или вставляем данные в таблицу symbols
        cursor.execute('''
            UPDATE symbols
            SET lastPrice = ?, volumeUsdt = ?
            WHERE symbol = ?
        ''', (last_price, volume_usdt, symbol))
        print(f"Данные для {symbol} успешно обновлены last_price={last_price}, volume_usdt={volume_usdt}")
    else:
        print(f"Нет данных last_price, volume_usdt для символа {symbol}")
    conn_db.commit()
    if cursor is not None:
        cursor.close()

def symbol_data_processing(conn_db, symbol):
    """
    Определяем в какой диапазон попала текущая цена. Первая треть вторая треть или третья треть.
    """
    cursor = conn_db.cursor()

    # Получаем максимальную и минимальную цены для символа из таблицы kline_history
    cursor.execute('''
    SELECT MAX(high), MIN(low) 
    FROM kline_history 
    WHERE symbol = ?
    ''', (symbol,))
    result = cursor.fetchone()

    if result and result[0] is not None and result[1] is not None:
        max_price = result[0]
        min_price = result[1]

        # Рассчитываем firstLine, secondLine и middleLine
        first_line = min_price + (max_price - min_price) / 3
        second_line = min_price + 2 * (max_price - min_price) / 3
        middle_line = (max_price + min_price) / 2

        # Получаем текущее время в unixtime
        date_last_check = int(datetime.now().timestamp())

        # Обновляем или вставляем данные в таблицу symbols
        cursor.execute('''
        INSERT INTO symbols (symbol, maxPrice, minPrice, firstLine, secondLine, middleLine, dateLastCheck)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol) DO UPDATE SET 
            maxPrice = excluded.maxPrice,
            minPrice = excluded.minPrice,
            firstLine = excluded.firstLine,
            secondLine = excluded.secondLine,
            middleLine = excluded.middleLine,
            dateLastCheck = excluded.dateLastCheck
        ''', (symbol, max_price, min_price, first_line, second_line, middle_line, date_last_check))
        cursor.execute('''
            UPDATE symbols
            SET lastPrice = ?, volumeUsdt = ?
            WHERE symbol = ?
        ''', (max_price, min_price, first_line, second_line, middle_line, date_last_check, symbol))
        print(f"Данные для {symbol} успешно обновлены max_price={max_price}, min_price={min_price}, "
              f"first_line={first_line}, second_line={second_line}, middle_line={middle_line}, "
              f"date_last_check={date_last_check}")
    else:
        print(f"Нет данных max_price, min_price, first_line, second_line, "
              f"middle_line, date_last_check для символа {symbol}")
    conn_db.commit()
    cursor.close()


if __name__ == '__main__':
    main()

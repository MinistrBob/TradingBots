from pybit.unified_trading import HTTP
import json
import sqlite3
import traceback
from settings import app_settings as appset
from sqlite_db import create_database, update_date_last_check
from utils import unixtime_to_datetime, get_current_unixtime
from datetime import datetime, timezone


def load_data_to_db():
    """
    Получает список торговых пар с биржи и по каждой паре загружает историю свечей 1D в БД, получает текущие параметры
    для пары, вычисляет различные параметры по полученным данным.
    :return:
    """
    # Цикл по всем монетам
    symbols_list = get_symbols_list()
    for symbol in symbols_list:
        print(f"\n\nОбработка пары: {symbol}")
        get_kline_history(symbol)
        get_tickers(symbol)
        symbol_data_processing(symbol)


def get_symbols_list():
    symbols = appset.bybit_api.get_instruments_info(category='spot')
    # print(json.dumps(symbols, indent=4))
    # file_path = r'c:\MyGit\TradingBots\Bybit\spot_symbols.json'
    # with open(file_path, 'r', encoding='utf-8') as f:
    #     symbols = json.load(f)
    # print(symbols)
    # print(len(symbols["result"]["list"]))
    # Extract all symbols where quoteCoin is USDT
    usdt_symbols = [item["symbol"] for item in symbols["result"]["list"] if item["quoteCoin"] == "USDT"]
    # Sort the list of symbols alphabetically
    usdt_symbols_sorted = sorted(usdt_symbols)
    # Print the filtered symbols
    # print(len(usdt_symbols_sorted), usdt_symbols_sorted)
    print(f"Всего {len(usdt_symbols_sorted)} USDT пар")
    return usdt_symbols_sorted


def batch_insert_klines_to_db(symbol, klines):
    """
    Вставляет несколько свечей в базу данных в одной операции.
    Если запись с таким startTime и symbol уже существует, обновляет данные.
    """
    cursor = None
    try:
        cursor = appset.conn_db.cursor()
        # Подготовка данных для batch-вставки
        data_to_insert = [
            (
                int(kline[0]),  # startTime
                symbol,
                float(kline[1]),  # open
                float(kline[2]),  # high
                float(kline[3]),  # low
                float(kline[4]),  # close
                float(kline[5]),  # volume
                float(kline[6])  # turnover
            ) for kline in klines
        ]

        # Выполняем batch-вставку с обработкой конфликта для пары startTime и symbol
        cursor.executemany('''
        INSERT INTO kline_history ([startTime], [symbol], [open], [high], [low], [close], [volume], [turnover])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT([startTime], [symbol]) DO UPDATE SET
            [open]=excluded.[open],
            [high]=excluded.[high],
            [low]=excluded.[low],
            [close]=excluded.[close],
            [volume]=excluded.[volume],
            [turnover]=excluded.[turnover]
        ''', data_to_insert)
        appset.conn_db.commit()
    except sqlite3.Error as e:
        raise Exception(f"Error in batch_insert_klines_to_db: {e}") from e
    finally:
        if cursor is not None:
            cursor.close()


def insert_kline_to_db(symbol, kline):
    """
    Вставляет одну свечу в базу данных.
    """
    cursor = None
    try:
        cursor = appset.conn_db.cursor()
        cursor.execute('''
        INSERT INTO kline_history ([startTime], [symbol], [open], [high], [low], [close], [volume], [turnover])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(kline[0]),  # startTime
            symbol,
            float(kline[1]),  # open
            float(kline[2]),  # high
            float(kline[3]),  # low
            float(kline[4]),  # close
            float(kline[5]),  # volume
            float(kline[6])  # turnover
        ))
        appset.conn_db.commit()
    except sqlite3.IntegrityError:
        # Если запись с таким startTime уже существует, ничего не делаем
        print(f"Запись с startTime {kline[0]} уже существует в базе данных.")
    finally:
        if cursor is not None:
            cursor.close()


def get_kline_history(symbol):
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
        response = appset.bybit_api.get_kline(
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
            batch_insert_klines_to_db(symbol, klines)
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
            print("===========================")
            break
        # Устанавливаем новое начальное время для следующей итерации
        end_time = last_time - interval_ms
        print("===========================")
    update_date_last_check(symbol, date_last_check)


def get_tickers(symbol):
    """
    Получаем данные для торговой паре: Текущую цену и Объем в USDT за последние 24 часа.
    Вносим эти данные в таблицу symbols.
    """
    tickers = appset.bybit_api.get_tickers(category="spot", symbol=symbol)
    print(f"tickers={tickers}")
    last_price = float(tickers['result']['list'][0]['lastPrice'])
    volume_usdt = int(float(tickers['result']['list'][0]['turnover24h']))
    print(f"last_price={last_price}, volume_usdt={volume_usdt}")
    cursor = None
    if last_price is not None and volume_usdt is not None:
        cursor = appset.conn_db.cursor()
        # Обновляем или вставляем данные в таблицу symbols
        cursor.execute('''
            INSERT INTO symbols (symbol, lastPrice, volumeUsdt)
            VALUES (?, ?, ?)
            ON CONFLICT(symbol) DO UPDATE SET 
                lastPrice = excluded.lastPrice,
                volumeUsdt = excluded.volumeUsdt
        ''', (symbol, last_price, volume_usdt))
        appset.last_price = last_price
        appset.conn_db.commit()
        print(f"Данные для {symbol} успешно обновлены last_price={last_price}, volume_usdt={volume_usdt}")
    else:
        print(f"Нет данных last_price, volume_usdt для символа {symbol}")
    if cursor is not None:
        cursor.close()


def symbol_data_processing(symbol):
    """
    Определяем в какой диапазон попала текущая цена. Первая треть вторая треть или третья треть.
    """
    cursor = appset.conn_db.cursor()

    # Получаем максимальную и минимальную цены для символа из таблицы kline_history
    cursor.execute('''
    SELECT MAX(high), MIN(low), MIN(startTime)
    FROM kline_history 
    WHERE symbol = ?
    ''', (symbol,))
    result = cursor.fetchone()

    if result and result[0] is not None and result[1] is not None and result[2] is not None:
        max_price = result[0]
        min_price = result[1]
        start_time = result[2]

        # Рассчитываем firstLine, secondLine и middleLine
        first_line = min_price + (max_price - min_price) / 3
        second_line = min_price + 2 * (max_price - min_price) / 3
        middle_line = min_price + (max_price - min_price) / 2

        # Определяем в какой range попадет текущая цена
        level = None
        if min_price <= appset.last_price < first_line:
            level = 1
        if first_line <= appset.last_price < middle_line:
            level = 2
        if middle_line <= appset.last_price < second_line:
            level = 3
        if appset.last_price >= second_line:
            level = 4

        # Сколько месяцев существует монета
        date_last_check = get_current_unixtime()
        # Вычисляем разницу в миллисекундах между двумя датами
        time_difference_milliseconds = date_last_check - start_time
        # Вычисляем разницу в месяцах
        months_diff = int(time_difference_milliseconds / appset.average_milliseconds_per_month)
        print(f"Примерная разница в месяцах: {months_diff}")

        # Сколько процентов от текущей цены до максимума.
        # Логика: на 1$ я куплю по текущей цене монеты, по максимуму я продам и получу больше $.
        # Вычитаю 1$ из полученной прибыли и высчитываю сколько эта прибыль в процентах.
        net_profit = (1 / appset.last_price) * max_price - 1
        print(f"net_profit={net_profit}")
        price_distance_to_max_pct = int(net_profit * 100)
        print(f"{price_distance_to_max_pct}% от текущей цены до максимума")

        # Обновляем данные в таблице symbols
        cursor.execute('''
            UPDATE symbols
            SET maxPrice = ?, minPrice = ?, firstLine = ?, secondLine = ?, middleLine = ?, 
            dateLastCheck = ?, level = ?, monthsDiff = ?, priceDistanceToMaxPct = ? 
            WHERE symbol = ?
        ''', (max_price, min_price, first_line, second_line, middle_line, date_last_check, level, months_diff,
              price_distance_to_max_pct, symbol))
        appset.conn_db.commit()
        print(f"Данные для {symbol} успешно обновлены max_price={max_price}, min_price={min_price}, "
              f"first_line={first_line}, second_line={second_line}, middle_line={middle_line}, "
              f"date_last_check={date_last_check}, level={level}, months_diff={months_diff}, "
              f"price_distance_to_max_pct={price_distance_to_max_pct}")
    else:
        print(f"Нет данных max_price, min_price для символа {symbol}")
    if cursor is not None:
        cursor.close()


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        load_data_to_db()
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)


if __name__ == '__main__':
    main()
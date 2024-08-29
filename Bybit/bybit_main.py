from pybit.unified_trading import HTTP
import json
import time
from datetime import datetime


def format_timestamp(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%d.%m.%Y %H:%M:%S:%f')[:-3] \
        if ts is not None \
        else 'Нет данных'


def main():
    session = HTTP(
        testnet=False,
        api_key=r"RFnhyD7SwLfxnrUHwf",
        api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
    )

    # print(session.get_orderbook(category="linear", symbol="BTCUSDT"))

    # symbols_list = get_symbols_list(session)

    # get_max_min_price(session, 'BTCUSDT')
    test1(session, 'BTCUSDT')

def get_symbols_list(session):
    symbols = session.get_instruments_info(category='spot')
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


def test1 (session, symbol):
    # Запрос исторических данных свечей с указанием временного диапазона
    response = session.get_kline(
        category="spot",
        symbol=symbol,
        interval="D",
        limit=1000,
    )
    klines = response['result']['list']
    print(klines[0])  # Печатаем первую свечу для отладки
    print(klines[1])

def get_max_min_price(session, symbol):
    max_price = float('-inf')
    min_price = float('inf')

    # Переменные для хранения времени
    earliest_time = None
    latest_time = None

    # Переменные для хранения времени максимальной и минимальной цены
    max_price_time = None
    min_price_time = None

    # Определяем текущее время в миллисекундах
    end_time = int(time.time() * 1000)  # Конечное время — текущее время
    interval_ms = 24 * 60 * 60 * 1000  # Интервал 1 день в миллисекундах
    start_time = 0  # Начальное время (0 для начала всей истории)



    while True:
        # Запрос исторических данных свечей с указанием временного диапазона
        response = session.get_kline(
            category="spot",
            symbol=symbol,
            interval="D",
            limit=1000,
            start=start_time,
            end=end_time
        )
        klines = response['result']['list']

        if not klines:
            break

        print(klines[0])  # Печатаем первую свечу для отладки

        # Обновляем максимум и минимум
        for kline in klines:
            timestamp = int(kline[0])  # Время начала свечи в миллисекундах
            high = float(kline[2])
            low = float(kline[3])

            if high > max_price:
                max_price = high
                max_price_time = timestamp  # Сохраняем время максимальной цены

            if low < min_price:
                min_price = low
                min_price_time = timestamp  # Сохраняем время минимальной цены

            # Определяем самое раннее и самое позднее время
            if earliest_time is None or timestamp < earliest_time:
                earliest_time = timestamp
            if latest_time is None or timestamp > latest_time:
                latest_time = timestamp

        # Обновляем start_time для следующего запроса
        last_time = int(klines[-1][0])  # Последнее время из текущих свечей
        if last_time >= end_time or len(klines) < 1000:
            break

        # Устанавливаем новое начальное время для следующей итерации
        start_time = last_time + interval_ms

    # Преобразуем временные метки в человекочитаемый формат
    earliest_time_str = format_timestamp(earliest_time)
    latest_time_str = format_timestamp(latest_time)
    max_price_time_str = format_timestamp(max_price_time)
    min_price_time_str = format_timestamp(min_price_time)

    # Выводим результаты
    print(f"Максимальная цена: {max_price} на {max_price_time_str}")
    print(f"Минимальная цена: {min_price} на {min_price_time_str}")
    print(f"Самое раннее время: {earliest_time_str}")
    print(f"Самое позднее время: {latest_time_str}")


if __name__ == '__main__':
    main()

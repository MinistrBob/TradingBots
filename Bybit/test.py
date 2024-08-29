from pybit.unified_trading import HTTP
import json
import time
from utils import unixtime_to_datetime, datetime_to_unixtime, get_current_unixtime


def main():
    session = HTTP(
        testnet=False,
        api_key=r"RFnhyD7SwLfxnrUHwf",
        api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
    )
    # test1(session, 'BTCUSDT')
    get_kline_history(session, 'BTCUSDT')

def get_kline_history(session, symbol):
    """
    Get kline history. Выборка происходит в обратном порядке от end к start.
    """
    end_time = get_current_unixtime()
    start_time = 0
    limit = 1000
    interval_ms = 24 * 60 * 60 * 1000  # Интервал 1 день в миллисекундах
    while True:
        # Запрашиваем следующие 1000 свечей
        response = session.get_kline(
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
            print(f"{unixtime_to_datetime(int(klines[0][0]))}\n{klines[0]}")
            print(f"{unixtime_to_datetime(int(klines[1][0]))}\n{klines[1]}")
            print("...")
            print(f"{unixtime_to_datetime(int(klines[-1][0]))}\n{klines[-1]}")
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

def test1 (session, symbol):
    # Запрос исторических данных свечей с указанием временного диапазона

    # end_time = 1625529600000 # 06.07.2021
    # start_time = 0
    # start_time = 1625443200000  # 05.07.2021
    # start_time = 1625097600000  # 01.07.2021
    # start_time = 1625529600000 # 06.07.2021
    limit = 1000
    response = session.get_kline(
        category="spot",
        symbol=symbol,
        interval="D",
        limit=limit,
        # start=start_time,
        end=end_time,
    )
    klines = response['result']['list']
    if len(klines) < limit:
        limit = len(klines)
    if klines:
        print(f"{unixtime_to_datetime(int(klines[0][0]))}\n{klines[0]}")
        print(f"{unixtime_to_datetime(int(klines[1][0]))}\n{klines[1]}")
        print(f"{unixtime_to_datetime(int(klines[limit - 1][0]))}\n{klines[limit - 1]}")
    else:
        print("klines is empty")


if __name__ == '__main__':
    main()

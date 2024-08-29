from pybit.unified_trading import HTTP
import json
import time
from utils import format_timestamp, datetime_to_unixtime


def main():
    session = HTTP(
        testnet=False,
        api_key=r"RFnhyD7SwLfxnrUHwf",
        api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
    )
    test1(session, 'BTCUSDT')



def test1 (session, symbol):
    # Запрос исторических данных свечей с указанием временного диапазона
    limit = 1000
    response = session.get_kline(
        category="spot",
        symbol=symbol,
        interval="D",
        limit=limit,
        start=0,
        # end=0,
    )
    klines = response['result']['list']
    if klines:
        print(f"{format_timestamp(int(klines[0][0]))}\n{klines[0]}")
        print(f"{format_timestamp(int(klines[1][0]))}\n{klines[1]}")
        print(f"{format_timestamp(int(klines[limit-1][0]))}\n{klines[limit-1]}")
    else:
        print("klines is empty")


if __name__ == '__main__':
    main()

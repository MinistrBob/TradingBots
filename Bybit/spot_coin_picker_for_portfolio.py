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

def get_kline_history(session, symbol):
    """
    Получение истории свечей для торговой пары для 1D.
    Выборка происходит в обратном порядке от end к start (от сегодня в прошлое).
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


if __name__ == '__main__':
    main()

from pybit.unified_trading import HTTP
import time

# Инициализация клиента
session = HTTP(
    testnet=True,
    api_key=r"RFnhyD7SwLfxnrUHwf",
    api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
)

# Получаем список всех торговых пар на споте с USDT
market_info = session.get_instruments_info(category='spot')
usdt_symbols = [item["symbol"] for item in market_info["result"]["list"] if item["quoteCoin"] == "USDT"]
# Sort the list of symbols alphabetically
usdt_pairs = sorted(usdt_symbols)


# Функция для получения исторических данных и нахождения максимума и минимума
def get_max_min_price(symbol):
    start_time = 0
    end_time = int(time.time())  # текущее время
    max_price = float('-inf')
    min_price = float('inf')

    while True:
        # Запрос исторических данных свечей
        response = session.query_kline(symbol=symbol, interval="1d", from_time=start_time, limit=200)
        klines = response['result']

        # Обновляем максимум и минимум
        for kline in klines:
            high = float(kline['high'])
            low = float(kline['low'])
            if high > max_price:
                max_price = high
            if low < min_price:
                min_price = low

        # Выход из цикла, если достигли конца данных
        if len(klines) < 200:
            break

        # Обновляем начало для следующего запроса
        start_time = klines[-1]['open_time']
        time.sleep(0.1)  # Задержка между запросами

    # Получаем текущую цену
    ticker_info = session.latest_information_for_symbol(symbol=symbol)
    current_price = float(ticker_info['result'][0]['last_price'])

    return max_price, min_price, current_price


# Формируем таблицу результатов
results = []

for pair in usdt_pairs:
    max_price, min_price, current_price = get_max_min_price(pair)
    results.append(f"{pair};{max_price};{min_price};{current_price}")

# Печатаем результаты
print("Pair;Max Price;Min Price;Current Price")
for result in results:
    print(result)

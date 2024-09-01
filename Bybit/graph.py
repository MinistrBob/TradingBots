import sqlite3
import pandas as pd
import mplfinance as mpf

# Подключаемся к базе данных
conn = sqlite3.connect('spot_coin_picker_for_portfolio.db')
symbol = '1INCHUSDT'

# Выполняем запрос и загружаем данные в DataFrame
query = f"""
SELECT 
    datetime(startTime / 1000, 'unixepoch') AS startDateFormatted,
    open, 
    high, 
    low, 
    close, 
    volume
FROM kline_history
WHERE symbol = '{symbol}';  -- Укажите символ, который вы хотите отобразить
"""

df = pd.read_sql_query(query, conn)

# Закрываем соединение с базой данных
conn.close()

# Преобразуем 'startDateFormatted' в формат datetime
df['startDateFormatted'] = pd.to_datetime(df['startDateFormatted'])

# Сортируем данные по дате в порядке возрастания
df.sort_values(by='startDateFormatted', inplace=True)

# Устанавливаем индекс DataFrame как дату
df.set_index('startDateFormatted', inplace=True)

# Переименовываем колонки для совместимости с mplfinance
df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

# Уровни цен для горизонтальных линий
price_levels = [0.20, 1.34, 1.91, 2.48, 3.63]

mpf.plot(df,
         type='candle',
         volume=True,
         style='binance',
         title=f'Candlestick Chart for {symbol}',
         datetime_format='%d.%m.%Y',
         hlines=dict(hlines=price_levels, colors=['blue', 'red', 'yellow', 'red', 'blue'], linewidths=1),
         # savefig='candlestick_chart.png'
         )
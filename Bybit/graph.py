import sqlite3
import os
import pandas as pd
import mplfinance as mpf
from datetime import datetime

from matplotlib.lines import lineStyles

from SETTINGS import app_settings as appset
import traceback
from sqlite_db import create_database, update_date_last_check
from utils import unixtime_to_datetime, get_current_unixtime
from datetime import datetime, timezone
from pybit.unified_trading import HTTP


def plot_graph(row, save_to_file=False):
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
    WHERE symbol = '{row[0]}';  -- Укажите символ, который вы хотите отобразить
    """
    df = pd.read_sql_query(query, appset.conn_db)

    # Преобразуем 'startDateFormatted' в формат datetime
    df['startDateFormatted'] = pd.to_datetime(df['startDateFormatted'])
    # Сортируем данные по дате в порядке возрастания
    df.sort_values(by='startDateFormatted', inplace=True)
    # Устанавливаем индекс DataFrame как дату
    df.set_index('startDateFormatted', inplace=True)
    # Переименовываем колонки для совместимости с mplfinance
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'},
              inplace=True)

    # Уровни цен для горизонтальных линий
    # ('SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995, 1, 34, 3471)
    price_levels = [row[5], row[6], row[7], row[8], row[4]]

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

    if save_to_file:
        full_path = os.path.join(appset.path_for_graphs, f'{row[11]}-{row[0]}-{current_datetime}.png')
        mpf.plot(df,
                 type='candle',
                 volume=True,
                 style='binance',
                 title=f'{row[0]} на {unixtime_to_datetime(row[1])[0:10]}   {row[11]}% {row[10]}мес.',
                 datetime_format='%d.%m.%Y',
                 hlines=dict(hlines=price_levels, colors=['blue', 'red', 'red', 'red', 'blue'], linestyle='--',
                             linewidths=1),
                 savefig=full_path,
                 )
    else:
        mpf.plot(df,
                 type='candle',
                 volume=True,
                 style='binance',
                 title=f'{row[0]} на {unixtime_to_datetime(row[1])[0:10]}   {row[11]}% {row[10]}мес.',
                 datetime_format='%d.%m.%Y',
                 hlines=dict(hlines=price_levels, colors=['blue', 'red', 'red', 'red', 'blue'], linestyle='--',
                             linewidths=1),
                 )


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        plot_graph(appset, (
        'SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995,
        1, 34, 3471))
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

from pybit.unified_trading import HTTP
import json
import sqlite3
import traceback
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check
from utils import unixtime_to_datetime, get_current_unixtime
from datetime import datetime, timezone
from graph import plot_graph


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        get_recommendation(appset)
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)

def get_recommendation(appset):
    """
    Получить список рекомендованных пар отобранных по определённым условиям.
    ('SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995, 1, 34, 3471)
    """
    cursor = appset.conn_db.cursor()
    # SQL-запрос
    query = """
    SELECT *
    FROM symbols
    WHERE monthsDiff > 8
      AND priceDistanceToMaxPct > 200
      AND (level = 1 OR level = 2)
      AND volumeUsdt > 1000000
    ORDER BY volumeUsdt DESC, priceDistanceToMaxPct DESC, level DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
        plot_graph(appset, row, save_to_file=True)
    if cursor is not None:
        cursor.close()


if __name__ == '__main__':
    main()
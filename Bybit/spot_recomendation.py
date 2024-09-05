from pybit.unified_trading import HTTP
import json
import sqlite3
import traceback
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check, select_recommendations_symbols, select_symbol
from utils import unixtime_to_datetime, get_current_unixtime
from datetime import datetime, timezone
from graph import plot_graph


def get_recommendation(save_to_file=False):
    """
    Получить список рекомендованных пар отобранных по определённым условиям.
    ('SANDUSDT', 1725235200000, 0.23768, 1118543, 8.48992, 0.20807, 2.968686666666667, 5.729303333333334, 4.348995, 1, 34, 3471)
    """
    results = select_recommendations_symbols()
    for row in results:
        print(row)
        plot_graph(row, save_to_file=save_to_file)


def get_graph(symbol, save_to_file=False):
    row = select_symbol(symbol)
    print(row)
    if row:
        plot_graph(row, save_to_file=save_to_file)
    else:
        print(f"Символ {symbol} не найден")


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        get_recommendation()
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

import traceback
from pybit.unified_trading import HTTP
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check
from spot_load_data_to_db import load_data_to_db
from spot_recomendation import get_recommendation, get_graph


def main():
    try:
        # Инициализация API и базы данных
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        list_symbols = ['REEFUSDT', 'HIGHUSDT', 'ARUSDT', 'NOTUSDT', 'SANDUSDT', 'EGLDUSDT', 'RAYUSDT', 'BAKEUSDT', 'CSPRUSDT', 'MINAUSDT', 'QTUMUSDT', 'FLOWUSDT', 'RDNTUSDT', 'KSMUSDT']
        for symbol in list_symbols:
            get_graph(symbol, save_to_file=True)
    except Exception:
        print(traceback.format_exc())
    finally:
        # Гарантированное закрытие соединения
        if hasattr(appset, 'conn_db') and appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)


if __name__ == "__main__":
    main()
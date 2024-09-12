from pybit.unified_trading import HTTP
import traceback
from settings import app_settings as appset
from sqlite_db import create_database, update_date_last_check, select_recommendations_symbols, select_symbol


def get_orders_list():
    orders = appset.bybit_api.get_open_orders(category="spot")
    print(f"orders={orders}")


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        get_orders_list()
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

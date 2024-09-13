from pybit.unified_trading import HTTP
import traceback
from settings import app_settings as appset
from sqlite_db import create_database, update_date_last_check, select_recommendations_symbols, select_symbol


def get_orders_list(cursor=None, orders=None):
    if orders is None:
        orders = []
    raw_orders = appset.bybit_api.get_open_orders(category="spot", limit=50, cursor=cursor)
    if raw_orders['retCode'] == 0:
        # print(f"orders={raw_orders}")
        for order in raw_orders['result']['list']:
            # print(order)
            orders.append(order)
        if 'nextPageCursor' in raw_orders['result'] and raw_orders['result']['nextPageCursor']:
            get_orders_list(cursor=raw_orders['result']['nextPageCursor'], orders=orders)
    else:
        raise Exception(f"Error: {raw_orders['retCode']} {raw_orders['retMsg']}")
    return orders



def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        orders = get_orders_list()
        for order in orders:
            print(order)
        print(f"Total number of orders: {len(orders)}")
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

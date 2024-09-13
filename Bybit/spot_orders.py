from pybit.unified_trading import HTTP
import traceback
from settings import app_settings as appset
from sqlite_db import create_database, orders_insert, orders_update, orders_delete, orders_select_for_compare


def get_orders_list_exchange(cursor=None, orders=None):
    """
    Получение списка ордеров с биржи. Функция рекурсивная, т.к. API возвращает не более 50 ордеров.
    :param cursor: Значение nextPageCursor.
    :param orders: Список ордеров.
    :return: Общий список ордеров с биржи.
    """
    if orders is None:
        orders = []
    raw_orders = appset.bybit_api.get_open_orders(category="spot", limit=50, cursor=cursor)
    if raw_orders['retCode'] == 0:
        # print(f"orders={raw_orders}")
        for order in raw_orders['result']['list']:
            # print(order)
            orders.append(order)
        if 'nextPageCursor' in raw_orders['result'] and raw_orders['result']['nextPageCursor']:
            get_orders_list_exchange(cursor=raw_orders['result']['nextPageCursor'], orders=orders)
    else:
        raise Exception(f"Error: {raw_orders['retCode']} {raw_orders['retMsg']}")
    return orders


def compare_orders(exchange_orders, db_orders):
    new_orders = []
    modified_orders = []
    deleted_orders = []

    if exchange_orders:
        exchange_orders_dict = {order['orderId']: order for order in exchange_orders}
    else:
        print("No orders from exchange")
        exchange_orders_dict = {}
    if db_orders:
        db_orders_dict = {order[0]: order[1] for order in db_orders}
    else:
        db_orders_dict = {}
        print("No orders from database")

    for orderId, order in exchange_orders_dict.items():
        if orderId not in db_orders_dict:
            new_orders.append(order)
        elif orderId in db_orders_dict and int(order['updatedTime']) > db_orders_dict[orderId]:
            modified_orders.append(order)

    for orderId, order in db_orders_dict.items():
        if orderId not in exchange_orders_dict:
            deleted_orders.append(order)

    return new_orders, modified_orders, deleted_orders


def main():
    try:
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()
        exchange_orders = get_orders_list_exchange()
        print(f"Total number of orders: {len(exchange_orders)}")
        db_orders = orders_select_for_compare()
        # db_orders=[('1774154455470868736', 1726231692192), ('1774154365662431488', 1726231681486), ...]
        new_orders, modified_orders, deleted_orders = compare_orders(exchange_orders, db_orders)
        orders_insert(new_orders)
        print(f"Total number of new orders: {len(new_orders)}")
        orders_update(modified_orders)
        print(f"Total number of modified orders: {len(modified_orders)}")
        orders_delete(deleted_orders)
        print(f"Total number of deleted orders: {len(deleted_orders)}")
    except Exception:
        print(traceback.format_exc())
        try:
            text = f"spot_orders Error: {traceback.format_exc()}"
            send_telegram_msg_post(text)
        except Exception:
            print(traceback.format_exc())
            text = f"spot_orders Не могу отправить ошибку в телеграм"
            send_telegram_msg_post(text)
    finally:
        # Гарантированное закрытие соединения
        if appset.conn_db is not None:
            try:
                appset.conn_db.close()
            except Exception as e:
                print("Ошибка при закрытии соединения:", e)


if __name__ == '__main__':
    main()

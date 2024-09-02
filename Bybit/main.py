import argparse
import traceback
from pybit.unified_trading import HTTP
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check


def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Программа для выбора торговых пар на spot Bybit")

    # Добавляем возможные аргументы
    parser.add_argument('--get-data', '-gd', action='store_true', help='Загрузить данные с биржи в базу данных')
    parser.add_argument('--get-recommendation', '-gr', action='store_true', help='Получить список рекомендованных пар')
    parser.add_argument('--get-graph', '-gg', type=str, help='Получить график по выбранной паре')

    # Разбираем аргументы
    args = parser.parse_args()

    try:
        # Инициализация API и базы данных
        appset.bybit_api = HTTP(
            testnet=False,
            api_key=appset.api_key,
            api_secret=appset.api_secret,
        )
        appset.conn_db = create_database()

        # Проверяем, какой аргумент был передан
        if args.get_data:
            get_data()
        elif args.get_recommendation:
            get_recommendation(appset)
        elif args.get_graph:
            get_graph(args.get_graph)
        else:
            common()

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

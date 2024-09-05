import argparse
import traceback
from pybit.unified_trading import HTTP
from SETTINGS import app_settings as appset
from sqlite_db import create_database, update_date_last_check
from spot_load_data_to_db import load_data_to_db
from spot_recomendation import get_recommendation, get_graph


def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Программа для выбора торговых пар на spot Bybit")

    # Добавляем возможные аргументы
    parser.add_argument('--load-data', '-ld', action='store_true', help='Загрузить данные с биржи в базу данных')
    parser.add_argument('--get-recommendation', '-gr', action='store_true', help='Получить список рекомендованных пар')
    parser.add_argument('--get-graph', '-gg', type=str, help='Получить график по выбранной паре')
    parser.add_argument('--save-file', '-sf', action='store_true', help='Сохранить график в файл')

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
        if args.load_data:
            load_data_to_db()
        elif args.get_recommendation:
            get_recommendation(save_to_file=args.save_file)
        elif args.get_graph:
            print(args.get_graph)
            print(args.save_file)
            get_graph(args.get_graph, save_to_file=args.save_file)
        else:
            load_data_to_db()
            get_recommendation(save_to_file=args.save_file)
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

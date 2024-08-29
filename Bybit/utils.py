from datetime import datetime

def format_timestamp(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%d.%m.%Y %H:%M:%S:%f')[:-3] if ts is not None else 'Нет данных'


def datetime_to_unixtime(date_str):
    # Определяем формат строки с датой
    date_format = "%d.%m.%Y %H:%M:%S"

    # Преобразуем строку в объект datetime
    dt = datetime.strptime(date_str, date_format)

    # Преобразуем datetime в unixtime
    unix_time = int(dt.timestamp())

    return unix_time

if __name__ == '__main__':
    ts = 1638576000000
    print(f"For timestamp {ts} date is {format_timestamp(ts)}")
    # Пример использования
    date_str = "04.12.2021 00:00:00"
    unix_time = datetime_to_unixtime(date_str)
    print(f"Unixtime для '{date_str}': {unix_time}")

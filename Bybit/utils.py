from datetime import datetime, timezone


def unixtime_to_datetime(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%d.%m.%Y %H:%M:%S:%f')[:-3] if ts is not None else 'Нет данных'

def unixtime_to_date(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%d.%m.%Y') if ts is not None else 'Нет данных'

def datetime_to_unixtime(date_str):
    # Определяем формат строки с датой
    date_format = "%d.%m.%Y %H:%M:%S"
    # Преобразуем строку в объект datetime с указанием UTC времени
    dt = datetime.strptime(date_str, date_format).replace(tzinfo=timezone.utc)
    # Преобразуем datetime в unixtime
    unix_time = int(dt.timestamp() * 1000)  # Приводим к миллисекундам для соответствия
    return unix_time


def get_current_unixtime():
    return datetime_to_unixtime(datetime.utcnow().strftime('%d.%m.%Y 00:00:00'))


if __name__ == '__main__':
    # unixtime to date
    ts = 1725135919
    print(f"For timestamp {ts} date is {unixtime_to_datetime(ts)}")

    # date to unixtime
    date_str = "06.07.2021 00:00:00"
    unix_time = datetime_to_unixtime(date_str)
    print(f"Unixtime для '{date_str}': {unix_time}")

    # Получаем текущую дату
    current_date = get_current_unixtime()
    # Преобразуем текущую дату в Unix Time
    unix_time = datetime_to_unixtime(current_date)
    print(f"Unix Time для текущей даты '{current_date}': {type(unix_time)} {unix_time}")

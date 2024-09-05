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

def subtract_one_list_from_another():
    list1 = ['1INCH', '5IRE', 'AAVE', 'ADA', 'APE', 'APT', 'ARB', 'ARKM', 'ATOM', 'AVAX', 'BLUR', 'CORE', 'CRV', 'DOGE',
             'DOT', 'DYDX', 'ENS', 'EOS', 'FET', 'FIL', 'FMB', 'FTM', 'GALA', 'GMT', 'HBAR', 'HNT', 'ICP', 'IMX', 'INJ',
             'JASMY', 'LDO', 'LINK', 'LMWR', 'LTC', 'MASK', 'MATIC', 'MEME', 'NEAR', 'OP', 'ORDI', 'POL', 'PPT', 'PYTH',
             'ROOT', 'RUNE', 'SEI', 'SFUND', 'SHIB', 'SNX', 'SSV', 'TIA', 'TOKEN', 'TOMI', 'UNI', 'WLD', 'WWY', 'XCAD',
             'XLM']
    list2 = ['1INCH', 'ADA', 'AR', 'ARB', 'AVAX', 'BAKE', 'BLUR', 'CRV', 'CSPR', 'DOT', 'EGLD', 'ENS', 'FET', 'FIL',
             'FLOW', 'FTM', 'GALA', 'HBAR', 'HIGH', 'ICP', 'JASMY', 'KSM', 'MINA', 'NEAR', 'NOT', 'ORDI', 'QTUM', 'RAY',
             'RDNT', 'REEF', 'RUNE', 'SAND', 'UNI', 'XLM']
    result = list(set(list2) - set(list1))
    print(result)



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

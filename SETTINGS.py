import os

DEBUG = False
PROFILE = 'DEV'
# debug = os.getenv('APP_DEBUG')
# if debug and debug.upper() == "TRUE":
#     DEBUG = True
# else:
#     DEBUG = False
#
# # Название профайла\среды должно быть обязательно
# profile = os.getenv('APP_PROFILE')
# if profile:
#     PROFILE = profile.upper()
# else:
#     raise Exception("Не определена переменная окружения APP_PROFILE")
#     exit(1)

# Настройки по умолчанию. Общие для всех профайлов. Настройки профайлов перекрывают эти настройки.
default_settings = dict(
    # Main settings
    # work_dir = sys.path[0],  # Рабочая папка = папке откуда запускается main.py, обычно это /home/ci/platform.
    # Определяется в начале main.py
    DEBUG=DEBUG,
    profile=PROFILE,
    bybit_api=None,
    conn_db=None,
    last_price=0,
    # Среднее количество дней в месяце за один год, учитывая високосные годы 30.44 * 24 * 60 * 60
    average_seconds_per_month = 2630016,
    api_key=r"RFnhyD7SwLfxnrUHwf",
    api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
)

# ~~~~ Настройки конкретных профайлов ~~~~
profile_settings = {}
# Настройки профайлов перекрывают настройки по умолчанию.
if PROFILE == 'DEV':
    profile_settings = dict(
        DEBUG=True,
    )

# Объединение общих настроек и настроек конкретного профайла
settings = {**default_settings, **profile_settings}


class Settings(object):
    """
    Класс настроек приложения.
    Singleton-класс, который позволяет иметь только один экземпляр.
    """
    _instance = None  # Статическая переменная для хранения единственного экземпляра

    def __new__(cls, iterable=(), **kwargs):
        if cls._instance is None:  # Проверка на наличие существующего экземпляра
            cls._instance = super(Settings, cls).__new__(cls)  # Создание экземпляра, если его нет
            cls._instance.__dict__.update(iterable, **kwargs)  # Инициализация экземпляра
        return cls._instance  # Возврат единственного экземпляра

    def __str__(self):
        return str(self.__dict__)


def get_settings():
    """
    Процедура возвращает настройки приложения в виде класса.
    :return:
    """
    return Settings(settings)


app_settings = get_settings()

if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(indent=2)
    print(f"DEBUG={DEBUG}")
    print(f"PROFILE={PROFILE}")
    print("\n" + "=" * 80 + "\nDefault settings\n" + "=" * 80)
    pp.pprint(default_settings)
    print("\n" + "=" * 80 + f"\nProfile {PROFILE} settings\n" + "=" * 80)
    pp.pprint(profile_settings)
    # print("\n" + "=" * 80 + "\nApp Settings\n" + "=" * 80)
    # pp.pprint(settings)

    s = Settings(settings)
    print("\n" + "=" * 80 + "\nClass Settings\n" + "=" * 80)
    pp.pprint(s.__dict__)

    appset = get_settings()
    print("\n" + "=" * 80 + "\nApp Settings\n" + "=" * 80)
    pp.pprint(appset)

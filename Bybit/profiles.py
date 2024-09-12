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
    # Среднее количество миллисекунд в месяце, учитывая високосные годы 30.44 * 24 * 60 * 60 * 1000
    average_milliseconds_per_month = 2630016000,
    api_key=r"RFnhyD7SwLfxnrUHwf",
    api_secret=r"JI5joaLGQ9KZsrjKDTAHfiP50gsq8DTmVE6l",
)

# ~~~~ Настройки конкретных профайлов ~~~~
profile_settings = {}
# Настройки профайлов перекрывают настройки по умолчанию.
if PROFILE == 'DEV':
    profile_settings = dict(
        DEBUG=True,
        path_for_graphs=r"c:\!SAVE\bybit_recomendation",
    )

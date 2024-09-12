import os
from profiles import default_settings, profile_settings

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
            # Проверка существования пути и создание его при необходимости
            cls._instance._ensure_path_exists('path_for_graphs')
        return cls._instance  # Возврат единственного экземпляра

    def _ensure_path_exists(self, path_key):
        """
        Проверяет, существует ли путь, и создает его, если нет.
        :param path_key: Ключ пути в словаре настроек.
        """
        path = self.__dict__.get(path_key)
        if path and not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Путь '{path}' создан.")
            except OSError as e:
                print(f"Ошибка при создании пути '{path}': {e}")
        elif path:
            print(f"Путь '{path}' уже существует.")

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
    print("\n" + "=" * 80 + "\nDefault settings\n" + "=" * 80)
    pp.pprint(default_settings)
    print("\n" + "=" * 80 + f"\nProfile settings\n" + "=" * 80)
    pp.pprint(profile_settings)
    # print("\n" + "=" * 80 + "\nApp Settings\n" + "=" * 80)
    # pp.pprint(settings)

    s = Settings(settings)
    print("\n" + "=" * 80 + "\nClass Settings\n" + "=" * 80)
    pp.pprint(s.__dict__)

    appset = get_settings()
    print("\n" + "=" * 80 + "\nApp Settings\n" + "=" * 80)
    pp.pprint(appset)

from cryptorg import Api
from settings import app_settings as appset


def main():

    cryptorg = Api(appset.api_key, appset.api_secret)

    bot_list = cryptorg.bot_list()
    print(bot_list)


if __name__ == '__main__':
    main()

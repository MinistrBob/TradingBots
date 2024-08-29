from cryptorg_futures import Api
from settings import app_settings as appset


def main():
    # Cryptorg API instance
    cryptorg = Api(appset.api_key, appset.api_secret)

    # Futures Access List.
    # access = cryptorg.access()
    # print(access)

    # Get list of all user's bots.
    bot_list = cryptorg.bot_list()
    print(bot_list)




if __name__ == '__main__':
    main()

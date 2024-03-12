from cryptorg import Api
from settings import app_settings as appset


def main():
    cryptorg = Api(appset.apiKey, appset.apiSecret)

    """ First arg must be an array of parrams """
    """ Second arg must be an array of attributes """

    print(cryptorg.botList())


if __name__ == '__main__':
    main()

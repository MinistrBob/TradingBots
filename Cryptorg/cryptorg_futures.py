import requests
import json
import time
import hashlib
import base64
import hmac
from settings import app_settings as appset


class Api:
    """
    Class for Cryptorg API for futures
    """

    api_key = ''
    api_secret = ''
    api_url = appset.api_url

    def __init__(self, api_key, api_secret):
        """
        Cryptorg api constructor
        :param api_key:
        :param api_secret:
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def access(self):
        """
        Futures Access List (get accessId).
        :return:
        """
        return self.send_request('GET', 'bot-futures/access-list')

    def bot_list(self):
        """
        Get list of all user's bots.
        :return:
        """
        return self.send_request('GET', 'bot-futures/all', 'exchange=CRYPTORG_FUTURES')

    def send_request(self, method, url, query='', params=''):
        """
        Send request to api.cryptorg.net. Response structure is:
        {
            "isSuccess": true,
            "errorMessage": "",
            "data": "Command was sent" (list of dictionaries or str)
        }
        :param method: HTTP method - 'GET' or 'POST'.
        :param url: API method url (example, for Get list of all user's bots: 'bot-futures/all').
        :param query: API method query parameters (example, for Get list of all user's bots: 'exchange=CRYPTORG_FUTURES').
        :param params: API method body parameters.
        :return: dict from response.
        """
        nonce = int(time.time())
        str_sign = f'/{url}/{nonce}/{query}'
        ctg_api_signature = hmac.new(self.api_secret.encode('utf-8'), base64.b64encode(str_sign.encode('utf-8')),
                                     hashlib.sha256).hexdigest()
        headers = {
            "CTG-API-SIGNATURE": f'{ctg_api_signature}',
            "CTG-API-KEY": f'{self.api_key}',
            "CTG-API-NONCE": f'{nonce}'
        }
        if query == '':
            sign_url = self.api_url + url
        else:
            sign_url = self.api_url + url + '?' + query

        # send request
        if method == 'GET':
            response = requests.get(url=sign_url, headers=headers)
        elif method == 'POST':
            response = requests.post(url=sign_url, headers=headers, json=params)
        # print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        return json.loads(response.text)  # return dict

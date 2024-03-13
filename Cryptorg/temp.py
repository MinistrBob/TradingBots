    """ GetCryptorg.net current status """

    def status(self):
        return self.send_request('GET', 'api/status')

    """ Get list of user's bots """

    def botList(self):
        return self.send_request('GET', 'bot-futures/all', 'exchange=CRYPTORG_FUTURES')

    """ Get bot details """

    def botInfo(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/info', query)

    """ Advanced create bot """

    def createBot(self, params, attributes):

        try:
            query = "pair=" + params['pair'] + "&exchange=" + params['exchange']
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('POST', 'bot/create', query, attributes)

    """ Create bot with preset """

    def createPreset(self, params, attributes):

        try:
            query = "pair=" + params['pair'] + "&exchange=" + params['exchange']
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('POST', 'bot/create-preset', query, attributes)

    """ Update bot settings """

    def updateBot(self, params, attributes):

        try:
            query = "pair=" + params['pair'] + "&botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('POST', 'bot/configure', query, attributes)

    """ Delete bot """

    def deleteBot(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/delete', query)

    """ Activate bot """

    def activateBot(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/activate', query)

    """ Deactivate bot """

    def deactivateBot(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/deactivate', query)

    """ Start bot force"""

    def startBotForce(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/start-force', query)

    """ Get bot logs """

    def getBotLogs(self, params):

        try:
            query = "botId=" + str(params['botId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'bot/logs', query)

    """ Freeze deal """

    def freezeDeal(self, params):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'deal/freeze', query)

    """ Freeze deal """

    def unFreezeDeal(self, params):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'deal/unfreeze', query)

    """ Update TakeProfit """

    def updateTakeProfit(self, params):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'deal/update-take-profit', query)

    """ Cancel deal """

    def cancelDeal(self, params):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'deal/cancel', query)

    """ Get deal info """

    def dealInfo(self, params):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'deal/info', query)

    """ Get analytics """

    def getAnalytics(self, params=''):

        try:
            query = "dealId=" + str(params['dealId'])
            pass

        except Exception as e:
            return {'status': 'ok', 'result': 'false', 'message': e}

        else:
            return self.send_request('GET', 'analytics/get', query)

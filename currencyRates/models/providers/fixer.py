from .provider import Provider
import requests

class Fixer:
    def getExchangeRate(self, source_currency, exchanged_currency, valuation_date):
        try:
            # We take the token and the url for Fixer API from the settings file
            fixer = Provider.objects.filter(name='Fixer').first()
            if not fixer:
                raise Exception('provider.invalid')

            token = fixer.token
            url = fixer.url

            # We make a request to the Fixer API to get the currency exchange rate for the given date
            endpoint = url + valuation_date + '?access_key='+token+'&base='+source_currency+'&symbols='+exchanged_currency
            response = requests.get(endpoint)
            print("Obtengo los datos de fixer.io")

            return {'status': True, 'value': response.content}
        except Exception as e:
            return {'status': False, 'value': e}
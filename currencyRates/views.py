from rest_framework.views import APIView
from .serializer import CurrencyRateListSerializer, CurrencyExchangeAmountSerializer#, TimeWeightedRateSerializer
from .models.currencyExchangeRate import CurrencyExchangeRate
from rest_framework.response import Response
from rest_framework import generics, status, filters
from .tasks import get_exchange_rate_data
from django.utils import timezone
import currencyRates.utils as utils
from .models import Currency
from collections import defaultdict
import traceback


"""
Service to retrieve a List of currency rates for a specific time period
@parameters:  source_currency / date from / date to
@response: a time series list of rate values for each available Currency.
"""
class CurrencyRates(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # we take the needed params
            sourceCurrency = request.query_params['source_currency']
            dateFrom = request.query_params['date_from']
            dateTo = request.query_params['date_to']

            # First we check date parameters format
            if not dateFrom or not utils.checkDateFormat(dateFrom, '%Y-%m-%d'):
                raise ValueError('Required format: YYYY-MM-DD', 'date_from.invalid')

            if not dateTo or not utils.checkDateFormat(dateTo, '%Y-%m-%d'):
                raise ValueError('Required format: YYYY-MM-DD', 'date_to.invalid')

            if dateFrom >= dateTo:
                raise ValueError('Date from must be previous to Date to', 'dates.invalid')

            # Now we check if the given currency is supported by our system
            if not sourceCurrency or not Currency.objects.filter(code=sourceCurrency).first():
                validCurrencies = Currency.objects.all()
                raise ValueError('Invalid currency. Valid values: ' + ', '.join([c.code for c in validCurrencies]), 'source_currency.invalid')

            # Take the currencyExchange for the selected values
            queryset = CurrencyExchangeRate.objects.filter(valuation_date__gte=dateFrom, valuation_date__lte=dateTo, source_currency__code=sourceCurrency).all()
            if not queryset:
                # we have to request new values
                print('request value')

            # we have to group by currency
            values = defaultdict(list)
            for q in queryset:
                values[q.exchanged_currency.code].append(CurrencyRateListSerializer(q).data)

            data = {'success': True, 'data': values}
            return Response(data=data, status=status.HTTP_200_OK)

        except ValueError as err:
            data = {'success': False, 'parameter': err.args[1], 'error': err.args[0]}
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {'success': False, 'error': 'Error during the execution'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



"""
Service that Calculates (latest) amount in a currency exchanged into a different currency.
@parameters:  source_currency / amount / exchanged_currency
@response: an object containing at least the rate value between source and exchanges currencies.
"""
class CurrencyExchange(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # we take the needed params
            sourceCurrency = request.query_params['source_currency']
            amount = request.query_params['amount']
            exchangedCurrency = request.query_params['exchanged_currency']

            # First we check if source and exchange currency are supported by the system
            if not sourceCurrency or not Currency.objects.filter(code=sourceCurrency).first():
                validCurrencies = Currency.objects.all()
                raise ValueError('Invalid currency. Valid values: ' + ', '.join([c.code for c in validCurrencies]), 'source_currency.invalid')

            if not exchangedCurrency or not Currency.objects.filter(code=exchangedCurrency).first():
                validCurrencies = Currency.objects.all()
                raise ValueError('Invalid currency. Valid values: ' + ', '.join([c.code for c in validCurrencies]), 'exchanged_currency.invalid')

            # Check that the given amount has a decimal format
            amountDecimal = utils.checkDecimal(amount)
            if not amount or not amountDecimal:
                raise ValueError('Invalid amount. Valid values: numeric', 'amount.invalid')

            # Now we check if we have a exchange for the day of today
            today = timezone.localtime(timezone.now())
            todayString = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
            queryset = CurrencyExchangeRate.objects.filter(valuation_date=todayString, source_currency__code=sourceCurrency, exchanged_currency__code=exchangedCurrency).first()
            if not queryset:
                # we have to request new values
                print('request value')

            values = CurrencyExchangeAmountSerializer(queryset, context={'amount': amountDecimal}).data

            data = {'success': True, 'data': values}
            return Response(data=data, status=status.HTTP_200_OK)

        except ValueError as err:
            data = {'success': False, 'parameter': err.args[1], 'error': err.args[0]}
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {'success': False, 'error': 'Error during the execution'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


"""
Service to retrieve time-weighted rate of return for any given amount invested from a currency into another one from given date until today
@parameters: source_currency / amount / exchanged_currency / start_date
@response: an object containing at least the rate value between source and exchanges currencies.
"""
class TimeWeightedRate(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # we take the needed params
            sourceCurrency = request.query_params['source_currency']
            amount = request.query_params['amount']
            exchangedCurrency = request.query_params['exchanged_currency']
            startDate = request.query_params['start_date']

            # First we check if source and exchange currency are supported by the system
            if not sourceCurrency or not Currency.objects.filter(code=sourceCurrency).first():
                validCurrencies = Currency.objects.all()
                raise ValueError('Invalid source currency. Valid values: ' + ', '.join([c.code for c in validCurrencies]), 'source_currency.invalid')

            if not exchangedCurrency or not Currency.objects.filter(code=exchangedCurrency).first():
                validCurrencies = Currency.objects.all()
                raise ValueError('Invalid exchange currency. Valid values: ' + ', '.join([c.code for c in validCurrencies]), 'exchanged_currency.invalid')

            # Now we check date format
            if not startDate or not utils.checkDateFormat(startDate, '%Y-%m-%d'):
                raise ValueError('Required format: YYYY-MM-DD', 'startDate.invalid')

            # Check that the given amount has a decimal format
            amountDecimal = utils.checkDecimal(amount)
            if not amount or not amountDecimal:
                raise ValueError('Invalid amount. Valid values: numeric', 'amount.invalid')

            # We take the currency exchange rate for the given currency source & exchange and calculate the cashflow for each queryset
            queryset = CurrencyExchangeRate.objects.filter(valuation_date__gte=startDate,
                                                           source_currency__code=sourceCurrency,
                                                           exchanged_currency__code=exchangedCurrency).extra(select={'cash_flow': "rate_value * "+amount}).all()
            if not queryset:
                # we have to request new values
                print('request value')

            response = utils.calculate_twr(queryset)
            # values = TimeWeightedRateSerializer(queryset, context={'twr': twr}).data

            data = {'success': True, 'data': response}
            return Response(data=data, status=status.HTTP_200_OK)

        except ValueError as err:
            data = {'success': False, 'parameter': err.args[1], 'error': err.args[0]}
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            data = {'success': False, 'error': 'Error during the execution'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

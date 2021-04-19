from django.urls import path, register_converter
from .views import CurrencyRates, CurrencyExchange, TimeWeightedRate

CurrencyRates_patterns = ([
    path('currencyRates/', CurrencyRates.as_view(), name='getCurrencyRatesList'),
    path('currencyExchange/', CurrencyExchange.as_view(), name='getCurrencyExchange'),
    path('timeWeightedRate/', TimeWeightedRate.as_view(), name='getTWR')
], 'currencyRates')
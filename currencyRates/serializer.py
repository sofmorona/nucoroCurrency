from .models.currencyExchangeRate import CurrencyExchangeRate
from rest_framework import serializers


# Serializer for the view CurrencyRates
class CurrencyRateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['valuation_date', 'rate_value']


# Serializer for the view CurrencyExchange
class CurrencyExchangeAmountSerializer(serializers.ModelSerializer):
    exchange_value = serializers.SerializerMethodField('calculate_exchange')
    source_currency = serializers.StringRelatedField(many=False)
    exchanged_currency = serializers.StringRelatedField(many=False)

    def calculate_exchange(self, obj):
        amount = self.context.get("amount")
        return amount * obj.rate_value

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'rate_value', 'exchange_value']


# # Serializer for the view CurrencyExchange
# class TimeWeightedRateSerializer(serializers.ModelSerializer):
#     twr = serializers.SerializerMethodField('calculate_twr')
#     source_currency = serializers.StringRelatedField(many=False)
#     exchanged_currency = serializers.StringRelatedField(many=False)
#
#     def calculate_exchange(self, obj):
#         return self.context.get("amount")
#
#     class Meta:
#         model = CurrencyExchangeRate
#         fields = ['source_currency', 'exchanged_currency', 'rate_value', 'twr']
#         # depth = 1
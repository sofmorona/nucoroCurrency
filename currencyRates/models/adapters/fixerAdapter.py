from _code.currencyRates.models.providers.provider import Provider
from _code.currencyRates.models.providers.fixer import Fixer

class FixerAdapter(Provider):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface via composition.
    """

    def __init__(self, fixer: Fixer):
        self.fixer = fixer

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        self.fixer.getExchange(source_currency, exchanged_currency, valuation_date)
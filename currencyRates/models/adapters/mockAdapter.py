from _code.currencyRates.models.providers.provider import Provider
from _code.currencyRates.models.providers.mock import Mock

class MockAdapter(Provider):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface via composition.
    """

    def __init__(self, mock: Mock) -> None:
        self.mock = mock

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date) -> str:
        self.mock.getDummyExchange()
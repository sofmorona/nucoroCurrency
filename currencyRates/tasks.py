from celery import shared_task


@shared_task
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    provider.getExchange(source_currency, exchanged_currency, valuation_date)
    return 'True'
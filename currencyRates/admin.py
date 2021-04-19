from django.contrib import admin

# Register your models here.
from .models import Provider
from .models import Currency
from .models import CurrencyExchangeRate

admin.site.register(Provider)
admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
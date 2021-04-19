from django.db import models
import abc

class Provider(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    priority = models.BooleanField(default=False, unique=True)
    url = models.TextField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        pass
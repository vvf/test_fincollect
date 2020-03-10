from django.db import models


# Create your models here.
class Currency(models.Model):
    code = models.SlugField(max_length=10, null=False, primary_key=True)
    name = models.CharField(max_length=20, null=False)
    symbol = models.CharField(max_length=4, null=True)

    update_time = models.DateTimeField(auto_now=True)
    rate_to_russian_rub = models.DecimalField(decimal_places=4, max_digits=15, null=True)

    def __str__(self):
        return f'{self.name}: 1{self.symbol} = {self.rate_to_russian_rub} Rub'


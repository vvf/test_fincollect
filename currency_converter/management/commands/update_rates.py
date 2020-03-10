from threading import Thread

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime

from currency_converter.models import Currency


def is_rates_need_update(currency: Currency = None):
    if not currency:
        currency = Currency.objects.first()
    return (datetime.now(tz=currency.update_time.tzinfo) - currency.update_time).total_seconds() >= 86400

def check_rate_updates(currency: Currency = None):
    if not currency:
        currency = Currency.objects.first()
    if not is_rates_need_update(currency):
        return

    Thread(target=download_rates, name="Download rates").start()

def download_rates():
    resp = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')

    curr_dom = BeautifulSoup(resp.text, 'lxml')
    var_val = {
        ch.charcode.text.lower(): float(ch.value.text.replace(',', '.')) / float(ch.nominal.text)
        for ch in curr_dom.body.valcurs.find_all('valute')
    }
    for currency in Currency.objects.all():
        if currency.code.lower() not in var_val:
            continue
        currency.rate_to_russian_rub = var_val[currency.code.lower()]
        currency.save()


class Command(BaseCommand):
    help = 'Fetch currencies from cbrf'

    def handle(self, *args, **options):
        download_rates()

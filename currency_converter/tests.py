import json
from random import random

from django.http.response import JsonResponse
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from currency_converter.models import Currency


class TestConvertCurrency(TestCase):
    def setUp(self):
        Currency.objects.filter(code__in=['EUR', 'USD']).delete()
        usd = Currency.objects.create(
            code='USD',
            name='US dollar',
            symbol='$',
            rate_to_russian_rub=50
        )
        eur = Currency.objects.create(
            code='EUR',
            name='Euro',
            symbol='€',
            rate_to_russian_rub=100
        )

    def test_some_not_exists(self):
        url = reverse('currency_converter:convert', kwargs=dict(from_slug='usd', to_slug='EUR'))
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 404, 'No "usd" currency (only USD)')

    def test_convert_usd_to_eur_exists(self):
        url = reverse('currency_converter:convert', kwargs=dict(from_slug='USD', to_slug='EUR'))
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200, 'Both currency exists')

    def test_convert_usd_to_eur_valid(self):
        url = reverse('currency_converter:convert', kwargs=dict(from_slug='EUR', to_slug='USD'))
        resp: JsonResponse = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(resp.content)
        self.assertAlmostEqual(float(data['rate']), 2.0, 4)

    def tearDown(self):
        Currency.objects.filter(code__in=['EUR', 'USD']).delete()



class TestDownloadRates(TestCase):
    Currency.objects.filter(code__in=['EUR', 'USD']).delete()
    usd = Currency.objects.create(
        code='USD',
        name='US dollar',
        symbol='$',
    )
    eur = Currency.objects.create(
        code='EUR',
        name='Euro',
        symbol='€',
    )

    def test_fake_download_usd_and_eur(self):
        from currency_converter.management.commands.update_rates import download_rates
        from mock import patch, MagicMock, Mock
        with patch('requests.get') as requests_get:
            requests_get.return_value = Mock()
            usd_rate = round(random()*100, 4)
            eur_rate = round(random()*100, 4)
            requests_get.return_value.text = f'''<?xml version="1.0" encoding="windows-1251"?>
                <ValCurs Date="07.03.2020">
                <Valute ID="Test00"><NumCode>001</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal><Value>{usd_rate}</Value></Valute>
                <Valute ID="Test01"><NumCode>002</NumCode><CharCode>EUR</CharCode><Nominal>1</Nominal><Value>{eur_rate}</Value></Valute>
                </ValCurs>
            '''
            download_rates()
            rates_by_codes = {
                currency.code.lower(): currency.rate_to_russian_rub
                for currency in Currency.objects.all()
            }
            self.assertAlmostEqual(float(rates_by_codes['usd']), usd_rate, 4)
            self.assertAlmostEqual(float(rates_by_codes['eur']), eur_rate, 4)


    def test_real_download_usd_and_eur(self):
        from currency_converter.management.commands.update_rates import download_rates
        download_rates()

    def tearDown(self):
        Currency.objects.filter(code__in=['EUR', 'USD']).delete()

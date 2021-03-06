# Generated by Django 3.0.4 on 2020-03-08 19:55

from django.db import migrations


def setup_currencies(apps, schema_editor):
    Currency = apps.get_model("currency_converter", "Currency")
    data = (
        ("CZK", "Czech koruna", "Kč"),
        ("EUR", "Euro", "€"),
        ("PLN", "Polish złoty", "zł"),
        ("USD", "US dollar", "$")
    )
    for code, name, symbol in data:
        Currency.objects.create(
            code=code,
            name=name,
            symbol=symbol
        )
    from currency_converter.management.commands.update_rates import download_rates
    from mock import patch
    with patch("currency_converter.views.Currency") as views:
        views = Currency
        download_rates()


class Migration(migrations.Migration):
    dependencies = [
        ('currency_converter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_currencies),
    ]

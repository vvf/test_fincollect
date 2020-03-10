from django.urls import path

from currency_converter.views import ConverterView, IndexView

app_name = 'currency_converter'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('convert/<slug:from_slug>/<slug:to_slug>', ConverterView.as_view(), name='convert')

]

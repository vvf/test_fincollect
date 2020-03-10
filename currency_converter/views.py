from django.forms import model_to_dict
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from currency_converter.models import Currency


class ConverterView(View):
    def get(self, request, from_slug, to_slug):
        currency_rate_from = Currency.objects.filter(code=from_slug).first()
        currency_rate_to =  Currency.objects.filter(code=to_slug).first()
        if not currency_rate_from or not currency_rate_to \
                or not currency_rate_to.rate_to_russian_rub \
                or not currency_rate_from.rate_to_russian_rub:
            raise Http404(f'No currencies or rates for {from_slug} nor {to_slug}')

        rate = round(currency_rate_from.rate_to_russian_rub / currency_rate_to.rate_to_russian_rub, 4)
        src_value = float(request.POST.get('value') or request.GET.get('value') or '0')
        dest_value = round(src_value * float(rate), 2)
        return JsonResponse({
            'from': model_to_dict(currency_rate_from),
            'to': model_to_dict(currency_rate_to),
            'rate': rate,
            'src': src_value,
            'dest': dest_value
        })


class IndexView(TemplateView):
    template_name = 'currency_converter/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs) or {}
        context['currencies'] = Currency.objects.all()
        return context
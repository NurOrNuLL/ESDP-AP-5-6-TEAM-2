from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import TradePointForm
from services.trade_point_services import TradePointServices
from models.nomenclature.models import Nomenclature
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect


class TradePointCreate(TemplateView):
    template_name = 'trade_point/trade_point_create.html'
    form_class = TradePointForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclature'] = Nomenclature.objects.all()
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            TradePointServices.create_trade_point(form.cleaned_data)
            return redirect('home', orgID=1)

        return render(request, self.template_name, {
            'form': form,
            'nomenclature': Nomenclature.objects.all()
        })


class TradePointList(TemplateView):
    template_name = 'trade_point/trade_points.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['trade_points'] = TradePointServices.get_trade_points(kwargs)
        return context

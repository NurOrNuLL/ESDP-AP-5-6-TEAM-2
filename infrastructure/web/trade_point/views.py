from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import TradePointForm
from services.trade_point_services import TradePointServices
from models.nomenclature.models import Nomenclature
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin


class TradePointCreate(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'trade_point/trade_point_create.html'
    form_class = TradePointForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclature'] = Nomenclature.objects.all()
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

    def post(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            TradePointServices.create_trade_point(form.cleaned_data)
            return redirect('home_redirect')

        return render(request, self.template_name, {
            'form': form,
            'nomenclature': Nomenclature.objects.all()
        })


class TradePointList(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'trade_point/trade_points.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['trade_points'] = TradePointServices.get_trade_points(kwargs)
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

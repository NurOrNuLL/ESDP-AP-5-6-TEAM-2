from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from services.employee_services import EmployeeServices
from .forms import TradePointForm
from services.trade_point_services import TradePointServices
from services.nomenclature_services import NomenclatureService
from models.nomenclature.models import Nomenclature
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from concurrency.exceptions import RecordModifiedError
from concurrency.api import disable_concurrency
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class TradePointCreate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'trade_point/trade_point_create.html'
    form_class = TradePointForm

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclature'] = Nomenclature.objects.all()
        context['orgID'] = self.kwargs['orgID']
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
            return redirect('nomenclature_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])

        return render(request, self.template_name, {
            'form': form,
            'nomenclature': Nomenclature.objects.all(),
            'tpID': EmployeeServices.get_attached_tradepoint_id(request, request.user.uuid)
        })


class TradePointList(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'trade_point/trade_points.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['trade_points'] = TradePointServices.get_trade_points(kwargs)
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class TradePointUpdate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'trade_point/trade_point_update.html'
    form_class = TradePointForm

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**self.kwargs)
        context['tpID'] = self.kwargs['tpID']
        context['orgID'] = self.kwargs['orgID']
        context['nomenclatures'] = NomenclatureService.get_nomenclatures_by_organization(self.kwargs)
        return context

    def get_inital(self, trade_pointID: int) -> dict:
        trade_point = TradePointServices.get_trade_point_by_clean_id(trade_pointID)
        initial = {
            'version': trade_point.version,
            'name': trade_point.name,
            'address': trade_point.address,
            'nomenclature': trade_point.nomenclature.all(),
        }
        return initial

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)
        context = self.get_context_data(**self.kwargs)
        form = self.form_class(initial=self.get_inital(trade_pointID=self.kwargs['trade_pointID']))
        context['form'] = form
        context['trade_point'] = TradePointServices.get_trade_point_by_clean_id(tpID=self.kwargs['trade_pointID'])
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict
             ) -> HttpResponse or HttpResponseRedirect:
        trade_point = TradePointServices.get_trade_point_by_clean_id(self.kwargs['trade_pointID'])

        form = self.form_class(data=request.POST, instance=trade_point)

        if form.is_valid():
            try:
                TradePointServices.update_trade_point(trade_point, form.cleaned_data)
            except RecordModifiedError:
                context = self.get_context_data(**self.kwargs)
                context['form'] = form.cleaned_data
                context['trade_point'] = TradePointServices.get_trade_point_by_clean_id(tpID=self.kwargs['trade_pointID'])
                return render(request, template_name='trade_point/trade_point_update_compare.html', context=context)
            else:
                TradePointServices.update_trade_point(trade_point, form.cleaned_data)
                return redirect('trade_point_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data(**self.kwargs)
            context['form'] = form
            return render(request, template_name=self.template_name, context=context)


class TradePointUpdateConcurrecnyView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request: HttpRequest, *args: list, **kwargs: dict
             ) -> HttpResponse or HttpResponseRedirect:
        trade_point = TradePointServices.get_trade_point_by_clean_id(tpID=self.kwargs['trade_pointID'])
        with disable_concurrency(trade_point):
            trade_point.name = request.POST.get('name')
            trade_point.address = request.POST.get('address')
            trade_point.save()
            trade_point.nomenclature.set(request.POST.get('nomenclature'))
            return redirect('trade_point_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])

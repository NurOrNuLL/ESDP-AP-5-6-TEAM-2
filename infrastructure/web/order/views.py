from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView
from .forms import OrderForm, PaymentForm
from django.shortcuts import render, redirect
from models.order.models import ORDER_STATUS_CHOICES
from models.payment.models import PAYMENT_STATUS_CHOICES
from services.employee_services import EmployeeServices
from services.order_services import OrderService
from services.payment_services import PaymentService
from services.contractor_services import ContractorService
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointServices
from services.own_services import OwnServices
from infrastructure.web.trade_point.context_processor import trade_point_context
from typing import Dict, Any
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    trade_points = trade_point_context(request)

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        return render(request, self.template_name, self.get_context_data())


class HomeRedirectView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        return redirect('home', orgID=1, tpID=EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid))


class OrderCreateFromContractor(TemplateView):
    template_name = 'order/order_create.html'
    order_form_class = OrderForm
    payment_form_class = PaymentForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        context['own'] = OwnServices.get_own_by_id(self.kwargs)
        context['payment_statuses'] = PAYMENT_STATUS_CHOICES
        context['order_statuses'] = ORDER_STATUS_CHOICES
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        post_data = request.POST.copy()
        payment_data = {
            'payment_status': post_data['payment_status']
        }
        post_data.pop('payment_status')
        order_data = post_data
        payment_form = self.payment_form_class(payment_data)
        order_form = self.order_form_class(order_data)
        if order_form.is_valid() and payment_form.is_valid():
            trade_point = TradePointServices.get_trade_point_by_id(self.kwargs)
            contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
            own = OwnServices.get_own_by_id(self.kwargs)
            order_form.cleaned_data['trade_point'] = trade_point
            order_form.cleaned_data['contractor'] = contractor
            order_form.cleaned_data['own'] = own
            payment = PaymentService.create_payment(payment_form.cleaned_data)
            order_form.cleaned_data['payment'] = payment
            order = OrderService.create_order(order_form.cleaned_data)
            return redirect('order_detail', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'],
                            contrID=self.kwargs['contrID'], ownID=self.kwargs['ownID'], ordID=order.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['order_form'] = order_form
            context['payment_form'] = payment_form
            return render(request, template_name=self.template_name, context=context)



class OrderDetail(TemplateView):
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        context['own'] = OwnServices.get_own_by_id(self.kwargs)
        context['order'] = OrderService.get_order_by_id(self.kwargs['ordID'])
        return context

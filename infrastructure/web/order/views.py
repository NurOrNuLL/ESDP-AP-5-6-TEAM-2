import json
from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView

from .forms import (
    OrderForm, PaymentForm,
    OrderCreateFormStage1, OrderCreateFormStage2,
    OrderCreateFormStage3
)
from django.shortcuts import render, redirect
from models.order.models import ORDER_STATUS_CHOICES
from models.payment.models import PAYMENT_STATUS_CHOICES
from models.nomenclature.category_choices import CATEGORY_CHOICES
from services.employee_services import EmployeeServices
from services.order_services import OrderService
from services.payment_services import PaymentService
from services.contractor_services import ContractorService
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointServices
from services.own_services import OwnServices
from infrastructure.web.trade_point.context_processor import trade_point_context
from typing import Dict, Any, List
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin


class HomePageView(LoginRequiredMixin, ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'home.html'
    trade_points = trade_point_context(request)

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return render(request, self.template_name, self.get_context_data())


class HomeRedirectView(LoginRequiredMixin, ResetOrderCreateFormDataMixin, View):
    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return redirect('home', orgID=1, tpID=EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        ))


class OrderCreateViewStage1(TemplateView):
    template_name = 'order/order_create_stage1.html'
    form_class = OrderCreateFormStage1

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(self.kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data()

        contractor_id = request.session.get('contractor')
        own_id = request.session.get('own')

        if contractor_id and own_id:
            context['session_contractor'] = ContractorService.get_contractor_by_id(contractor_id)
            context['session_own'] = OwnServices.get_own_by_id({'ownID': own_id})
            context['owns'] = OwnServices.get_own_by_contr_id(contractor_id)

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['contractor'] = form.cleaned_data['contractor'].id
            request.session['own'] = form.cleaned_data['own'].id

            return redirect('order_create_stage2', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data()
            context['form'] = form

            return render(request, self.template_name, context)


class OrderCreateViewStage2(TemplateView):
    template_name = 'order/order_create_stage2.html'
    form_class = OrderCreateFormStage2

    def get_services(self, context: dict) -> Dict[str, List[dict]]:
        services = TradePointServices.get_trade_point_by_id(context).nomenclature.services
        filtered_data = {}

        for category in CATEGORY_CHOICES:
            filtered_data[f'{category[0]}'] = \
                [service for service in services if service['Категория'] == category[0]]

        return filtered_data

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        context['categories'] = CATEGORY_CHOICES
        context['services'] = self.get_services(context)

        employees = EmployeeServices.get_employee_by_tradepoint(
                tradepoint=TradePointServices.get_trade_point_by_id(self.kwargs)
            ).filter(role='Мастер')
        context['employees'] = [{"IIN": employee.IIN, "name": employee.name, "surname": employee.surname} for employee in employees]

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data()

        jobs = request.session.get('jobs')

        if jobs:
            context['session_jobs'] = json.dumps(jobs)

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['jobs'] = form.cleaned_data['jobs']

            return redirect('order_create_stage3', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data()
            context['form'] = form

            return render(request, self.template_name, context)


class OrderCreateViewStage3(TemplateView):
    template_name = 'order/order_create_stage3.html'
    form_class = OrderCreateFormStage3

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        context['payment_methods'] = PaymentService.get_payment_methods()

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        own = OwnServices.get_own_by_id({'ownID': request.session['own']})

        context = self.get_context_data()

        mileage = request.session.get('mileage')
        note = request.session.get('note')

        if own.is_part:
            if note:
                context['note'] = note
        else:
            if mileage and not note:
                context['session_mileage'] = mileage
            elif not mileage and note:
                context['session_note'] = note
            else:
                context['session_mileage'] = mileage
                context['session_note'] = note

        context['own'] = own

        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['mileage'] = form.cleaned_data['mileage']
            request.session['note'] = form.cleaned_data['note']

            return redirect('order_create_stage4', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data()
            context['form'] = form

            return render(request, self.template_name, context)


class OrderCreateViewStage4(TemplateView):
    template_name = 'order/order_create_stage4.html'

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def get_prices(self, jobs: List[Dict[Any, Any]]) -> List[int]:
        price_for_pay = 0
        full_price = 0

        for job in jobs:
            if job['Гарантия']:
                full_price += job['Цена услуги']
            else:
                price_for_pay += job['Цена услуги']
                full_price += job['Цена услуги']

        return [price_for_pay, full_price]

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data()
        context['contractor'] = ContractorService.get_contractor_by_id(request.session['contractor'])
        context['own'] = OwnServices.get_own_by_id({'ownID': request.session['own']})
        context['jobs'] = request.session['jobs']
        context['mileage'] = request.session['mileage']
        context['note'] = request.session['note']
        context['price_for_pay'], context['full_price'] = self.get_prices(request.session['jobs'])

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        prices = self.get_prices(request.session['jobs'])

        data = {
            'trade_point': TradePointServices.get_trade_point_by_id({'tpID': self.kwargs['tpID']}),
            'contractor': ContractorService.get_contractor_by_id(request.session['contractor']),
            'own': OwnServices.get_own_by_id({'ownID': request.session['own']}),
            'status': ORDER_STATUS_CHOICES[0][0],
            'price_for_pay': prices[0],
            'full_price': prices[1],
            'payment': PaymentService.create_unpaid_payment(),
            'note': request.session.get('note'),
            'mileage': request.session.get('mileage'),
            'jobs': request.session['jobs']
        }

        OrderService.create_order(data)

        del request.session['contractor']
        del request.session['own']
        del request.session['jobs']
        if request.session.get('note'): del request.session['note']
        if request.session.get('mileage'): del request.session['mileage']

        return redirect('home', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])


class OrderCreateFromContractor(TemplateView):
    template_name = 'order/order_create.html'
    order_form_class = OrderForm
    payment_form_class = PaymentForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(
            self.kwargs['contrID']
        )
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
            return redirect('order_detail', orgID=self.kwargs['orgID'],
                            tpID=self.kwargs['tpID'],
                            contrID=self.kwargs['contrID'],
                            ownID=self.kwargs['ownID'],
                            ordID=order.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['order_form'] = order_form
            context['payment_form'] = payment_form
            return render(request, template_name=self.template_name, context=context)


class OrderDetail(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(
            self.kwargs['contrID']
        )
        context['own'] = OwnServices.get_own_by_id(self.kwargs)
        context['order'] = OrderService.get_order_by_id(self.kwargs['ordID'])
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

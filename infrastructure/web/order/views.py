import ast
import json
from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView
from models.nomenclature.models import Nomenclature

from services.nomenclature_services import NomenclatureService

from .forms import (
    OrderCreateFormStage1, OrderCreateFormStage2,
    OrderCreateFormStage3, OrderUpdateForm
)
from datetime import datetime
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
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from rest_framework import generics, filters
from models.order.models import Order
from infrastructure.web.order.serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from concurrency.api import disable_concurrency
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class HomePageView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    trade_points = trade_point_context(request)

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        context['payment_statuses'] = PAYMENT_STATUS_CHOICES
        context['order_statuses'] = ORDER_STATUS_CHOICES
        context['order_dates'] = Order.objects.filter(trade_point_id=self.kwargs.get('tpID'))
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return render(request, self.template_name, self.get_context_data())


class MyPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'


class OrderFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request: HttpRequest, queryset: List[Order], view: View) -> List[Order]:
        try:
            request_date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
        except ValueError:
            filtered_orders = []

            for order in queryset:
                if order.own.is_part:
                    if (
                        request.GET.get('payment_status') in order.payment.payment_status
                        and request.GET.get('status') in order.status
                        and request.GET.get('search').lower() in order.contractor.name.lower()
                    ):
                        filtered_orders.append(order)
                else:
                    if (
                        request.GET.get('payment_status') in order.payment.payment_status
                        and request.GET.get('status') in order.status
                        and (request.GET.get('search').lower() in order.contractor.name.lower()
                             or request.GET.get('search').lower() in order.own.number.lower())
                    ):
                        filtered_orders.append(order)

            return filtered_orders
        else:
            filtered_orders = []

            for order in queryset:
                if order.own.is_part:
                    if (
                        request.GET.get('payment_status') in order.payment.payment_status
                        and request.GET.get('status') in order.status
                        and request.GET.get('search').lower() in order.contractor.name.lower()
                        and request_date.day == order.created_at.day
                        and request_date.month == order.created_at.month
                        and request_date.year == order.created_at.year
                    ):
                        filtered_orders.append(order)
                else:
                    if (
                        request.GET.get('payment_status') in order.payment.payment_status
                        and request.GET.get('status') in order.status
                        and (request.GET.get('search').lower() in order.contractor.name.lower()
                             or request.GET.get('search').lower() in order.own.number.lower())
                        and request_date.day == order.created_at.day
                        and request_date.month == order.created_at.month
                        and request_date.year == order.created_at.year
                    ):
                        filtered_orders.append(order)

            return filtered_orders


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = MyPagination
    filter_backends = [OrderFilterBackend, ]

    def get_queryset(self):
        trade_point_id = self.kwargs.get('tpID')
        return Order.objects.filter(trade_point_id=trade_point_id).order_by('-created_at')


class HomeRedirectView(LoginRequiredMixin, ResetOrderCreateFormDataMixin, View):
    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return redirect('home', orgID=1, tpID=EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        ))


class OrderCreateViewStage1(UserPassesTestMixin, TemplateView):
    template_name = 'order/order_create_stage1.html'
    form_class = OrderCreateFormStage1

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(self.kwargs)
        context['nomenclatures'] = \
            TradePointServices.get_trade_point_by_clean_id(self.kwargs['tpID']).nomenclature.all()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data()

        if request.GET.get('contractor') and request.GET.get('own'):
            request.session['contractor'] = request.GET.get('contractor')
            request.session['own'] = request.GET.get('own')

        nomenclature_id = request.session.get('nomenclature')
        contractor_id = request.session.get('contractor')
        own_id = request.session.get('own')

        if contractor_id:
            context['session_contractor'] = ContractorService.get_contractor_by_id(contractor_id)
        elif contractor_id and own_id:
            context['session_contractor'] = ContractorService.get_contractor_by_id(contractor_id)
            context['session_own'] = OwnServices.get_own_by_id({'ownID': own_id})
            context['owns'] = OwnServices.get_own_by_contr_id(contractor_id)

        if contractor_id and own_id and nomenclature_id:
            context['session_nomenclature'] = NomenclatureService.get_nomenclature_by_id(nomenclature_id)
            context['session_contractor'] = ContractorService.get_contractor_by_id(contractor_id)
            context['session_own'] = OwnServices.get_own_by_id({'ownID': own_id})
            context['owns'] = OwnServices.get_own_by_contr_id(contractor_id)

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['nomenclature'] = form.cleaned_data['nomenclature']
            request.session['contractor'] = form.cleaned_data['contractor'].id
            request.session['own'] = form.cleaned_data['own'].id

            return redirect('order_create_stage2', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data()
            context['form'] = form

            return render(request, self.template_name, context)


class OrderCreateViewStage2(UserPassesTestMixin, TemplateView):
    template_name = 'order/order_create_stage2.html'
    form_class = OrderCreateFormStage2

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_services(self, nomenclature: Nomenclature) -> Dict[str, List[dict]]:
        services = nomenclature.services
        filtered_data = {}

        for category in CATEGORY_CHOICES:
            filtered_data[f'{category[0]}'] = \
                [service for service in services if service['Категория'] == category[0]]

        return filtered_data

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        context['categories'] = CATEGORY_CHOICES

        employees = EmployeeServices.get_employee_by_tradepoint(
                tradepoint=TradePointServices.get_trade_point_by_id(self.kwargs)
            ).filter(role='Мастер')
        context['employees'] = [{"IIN": employee.IIN, "name": employee.name, "surname": employee.surname} for employee in employees]

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        nomenclature = \
            NomenclatureService.get_nomenclature_by_id(request.session.get('nomenclature'))

        context = self.get_context_data()
        context['services'] = self.get_services(nomenclature)

        jobs = request.session.get('jobs')

        if jobs:
            context['session_jobs'] = json.dumps(jobs)

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        nomenclature = \
            NomenclatureService.get_nomenclature_by_id(request.session.get('nomenclature'))
        form = self.form_class(request.POST)

        if form.is_valid():
            for job in form.cleaned_data['jobs']:
                if not job['Мастера']:
                    form.errors['jobs'] = 'Вы не выбрали мастеров!!!'

                    context = self.get_context_data()
                    context['services'] = self.get_services(nomenclature)
                    context['session_jobs'] = json.dumps(form.cleaned_data['jobs'])
                    context['form'] = form

                    return render(request, self.template_name, context)

            request.session['jobs'] = form.cleaned_data['jobs']

            return redirect('order_create_stage3', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
        else:
            form.errors['jobs'] = 'Вы не выбрали услуги!!!'

            context = self.get_context_data()
            context['services'] = self.get_services(nomenclature)
            context['form'] = form

            return render(request, self.template_name, context)


class OrderCreateViewStage3(UserPassesTestMixin, TemplateView):
    template_name = 'order/order_create_stage3.html'
    form_class = OrderCreateFormStage3

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

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


class OrderCreateViewStage4(UserPassesTestMixin, TemplateView):
    template_name = 'order/order_create_stage4.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

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
            'nomenclature': NomenclatureService.get_nomenclature_by_id(request.session['nomenclature']),
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


class OrderDetail(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        order = OrderService.get_order_by_id(self.kwargs['ordID'])

        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = order.contractor
        context['own'] = order.own
        context['order'] = order

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class OrderUpdateView(ResetOrderCreateFormDataMixin, UserPassesTestMixin, TemplateView):
    template_name = 'order/update.html'
    concurrency_template_name = 'order/concurrency_update.html'
    form_class = OrderUpdateForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_services(self, order: Order) -> Dict[str, List[dict]]:
        services = order.nomenclature.services
        filtered_data = {}

        for category in CATEGORY_CHOICES:
            filtered_data[f'{category[0]}'] = \
                [service for service in services if service['Категория'] == category[0]]

        return filtered_data

    def get_context_data_for_GET(self, form: OrderUpdateForm, order: Order, request: HttpRequest) -> Dict[str, Any]:
        context = self.get_context_data()
        context['form'] = form
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(request, request.user.uuid)
        context['ordID'] = order.id
        context['categories'] = CATEGORY_CHOICES
        context['services'] = self.get_services(order)

        employees = EmployeeServices.get_employee_by_tradepoint(
                tradepoint=TradePointServices.get_trade_point_by_id(self.kwargs)
            ).filter(role='Мастер')

        context['employees'] = [{"IIN": employee.IIN, "name": employee.name, "surname": employee.surname} for employee in employees]

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        order = OrderService.get_order_by_id(self.kwargs['ordID'])

        form = self.form_class(initial=OrderService.get_initial_for_update(order))

        context = self.get_context_data_for_GET(form, order, request)

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        order = OrderService.get_order_by_id(self.kwargs['ordID'])

        form = self.form_class(data=request.POST, instance=order)

        if form.is_valid():
            for job in form.cleaned_data['jobs']:
                if not job['Мастера']:
                    form.errors['jobs'] = 'Вы не выбрали мастеров!!!'
                    employees = EmployeeServices.get_employee_by_tradepoint(
                                    tradepoint=TradePointServices.get_trade_point_by_id(self.kwargs)
                                ).filter(role='Мастер')

                    context = self.get_context_data()
                    context['services'] = self.get_services(order)
                    context['categories'] = CATEGORY_CHOICES
                    context['employees'] = [{"IIN": employee.IIN, "name": employee.name, "surname": employee.surname} for employee in employees]
                    context['form'] = form
                    context['tpID'] = EmployeeServices.get_attached_tradepoint_id(request, request.user.uuid)
                    context['ordID'] = order.id

                    return render(request, self.template_name, context)

            try:
                order.jobs = form.cleaned_data['jobs']
                order.mileage = form.cleaned_data['mileage']
                order.note = form.cleaned_data['note']

                order.save()
            except RecordModifiedError:
                context = self.get_context_data()
                context['tpID'] = EmployeeServices.get_attached_tradepoint_id(request, request.user.uuid)
                context['ordID'] = order.id
                context['current_data'] = OrderService.get_order_by_id(self.kwargs['ordID'])
                context['new_data'] = form.cleaned_data

                return render(request, self.concurrency_template_name, context)
            else:
                order.jobs = form.cleaned_data['jobs']
                order.mileage = form.cleaned_data['mileage']
                order.note = form.cleaned_data['note']

                order.save()

                return redirect('order_detail', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'], ordID=self.kwargs['ordID'])
        else:
            form.errors['jobs'] = 'Вы не выбрали услуги!!!'
            employees = EmployeeServices.get_employee_by_tradepoint(
                tradepoint=TradePointServices.get_trade_point_by_id(self.kwargs)
            ).filter(role='Мастер')

            context = self.get_context_data()
            context['form'] = form
            context['tpID'] = EmployeeServices.get_attached_tradepoint_id(request, request.user.uuid)
            context['ordID'] = order.id
            context['categories'] = CATEGORY_CHOICES
            context['services'] = self.get_services(order)
            context['employees'] = [{"IIN": employee.IIN, "name": employee.name, "surname": employee.surname} for employee in employees]

            return render(request, self.template_name, context)


class OrderUpdateConcurrencyView(UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def post(self, request: HttpRequest, *args: list, **kwargs: dict):
        order = OrderService.get_order_by_id(self.kwargs['ordID'])

        with disable_concurrency(order):
            order.jobs = ast.literal_eval(request.POST['jobs'])
            order.mileage = request.POST.get('mileage')
            order.note = request.POST.get('note')

            order.save()

            return redirect('order_detail', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'], ordID=self.kwargs['ordID'])

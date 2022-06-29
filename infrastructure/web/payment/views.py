from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDictKeyError

from models.payment.models import PAYMENT_STATUS_CHOICES
from services.order_services import OrderService
from services.organization_services import OrganizationService
from .forms import PaymentForm
from models.payment_method.models import PaymentMethod
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from models.order.models import Order
from services.employee_services import EmployeeServices


class OrderPayment(LoginRequiredMixin, UserPassesTestMixin, ResetOrderCreateFormDataMixin, TemplateView):
    """Создание оплаты заказ-наряда"""
    template_name = 'home.html'
    form_class = PaymentForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> dict:
        order = OrderService.get_order_by_id(self.kwargs['ordID'])
        context = super(OrderPayment, self).get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['payment_statuses'] = PAYMENT_STATUS_CHOICES
        context['order_id'] = order.pk
        context['details'] = order.payment.details
        context['order'] = order
        context['tpID'] = self.kwargs['tpID']
        form = PaymentForm()
        context['form'] = form
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            order_id = self.get_context_data().get('order_id')
            piked_order = Order.objects.get(pk=order_id)
            try:
                details = dict(cash=request.POST['details_cash'], cashless=request.POST['details_cashless'],
                               kaspi=request.POST['details_kaspi'])
                details['cashless'] = {'consignment': request.POST['consignment'], 'invoice': request.POST['invoice']}
            except MultiValueDictKeyError:
                details = {'cash': '', 'cashless': {'consignment': '', 'invoice': ''}, 'kaspi': ''}
            get_method = PaymentMethod.objects.get(pk=int(request.POST['method']))
            status = request.POST['payment_status']
            piked_order.payment.method = get_method
            piked_order.payment.payment_status = status
            piked_order.payment.details = details
            piked_order.payment.save()
            return render(request, self.template_name, self.get_context_data())
        else:
            context['form'] = form
            context['error'] = form.errors
            context['details'] = dict(cash=request.POST['details_cash'], cashless=request.POST['details_cashless'],
                                      kaspi=request.POST['details_kaspi'])
            return render(request, self.template_name, self.get_context_data())

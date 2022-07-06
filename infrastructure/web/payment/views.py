import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from models.payment.models import PAYMENT_STATUS_CHOICES
from services.order_services import OrderService
from services.organization_services import OrganizationService
from .forms import PaymentForm
from models.payment_method.models import PaymentMethod
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from models.order.models import Order
from services.employee_services import EmployeeServices
from models.payment.models import PAYMENT_JSON_FIELD_SCHEMA_CASHLESS, PAYMENT_JSON_FIELD_SCHEMA_KASPI
from services.nomenclature_services import NomenclatureService
from django.http.response import HttpResponse


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
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)

        if form.is_valid():
            order_id = self.get_context_data().get('order_id')
            piked_order = Order.objects.get(pk=order_id)
            payment_pk = int(request.POST['method'])
            if payment_pk == 1:
                details_cash = dict(cash=request.POST.get('details_cash'))
                get_method = PaymentMethod.objects.get(pk=payment_pk)
                status = request.POST['payment_status']
                piked_order.payment.method = get_method
                piked_order.payment.payment_status = status
                piked_order.payment.details = details_cash
                piked_order.payment.save()
                return render(request, self.template_name, self.get_context_data())
            elif payment_pk == 2:
                details_cashless = dict(cashless=request.POST.get('details_cashless'))
                details_cashless['cashless'] = {'consignment': request.POST.get('consignment'), 'invoice': request.POST.get('invoice')}
                get_method = PaymentMethod.objects.get(pk=payment_pk)
                validated_data = NomenclatureService.validate_json(
                    json.dumps(details_cashless), PAYMENT_JSON_FIELD_SCHEMA_CASHLESS
                )
                if validated_data:
                    status = request.POST['payment_status']
                    piked_order.payment.method = get_method
                    piked_order.payment.payment_status = status
                    piked_order.payment.details = details_cashless
                    piked_order.payment.save()
                else:
                    return HttpResponse(json.dumps({'error': 'Счет фактура или накладное заполнено не корректно, '
                                                             'максимальная длина 100 символов'}), content_type='application/json')
            elif payment_pk == 3:
                details_kaspi = dict(kaspi=request.POST.get('details_kaspi'))
                get_method = PaymentMethod.objects.get(pk=payment_pk)
                validated_data = NomenclatureService.validate_json(
                    json.dumps(details_kaspi), PAYMENT_JSON_FIELD_SCHEMA_KASPI
                )
                if validated_data:
                    status = request.POST['payment_status']
                    piked_order.payment.method = get_method
                    piked_order.payment.payment_status = status
                    piked_order.payment.details = details_kaspi
                    piked_order.payment.save()
                else:
                    return HttpResponse(json.dumps({'error': ' Возможно вы забыли выбрать каспи метод'}),
                                        content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error': 'Данный метод оплаты не существует'}),
                                    content_type='application/json')
            return render(request, self.template_name, self.get_context_data())


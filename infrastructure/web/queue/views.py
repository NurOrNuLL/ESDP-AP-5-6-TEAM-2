from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from infrastructure.web.queue.forms import QueueForm
from models.queue.models import QUEUE_STATUSES
from services.contractor_services import ContractorService
from services.employee_services import EmployeeServices
from services.queue_services import QueueService
from services.trade_point_services import TradePointService


class QueueCreate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'queue/queue_create.html'
    form_class = QueueForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(self.kwargs)
        context['orgID'] = self.kwargs['orgID']
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)
        context = self.get_context_data(**self.kwargs)
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)
        if form.is_valid():
            trade_point = TradePointService.get_trade_point_by_clean_id(self.kwargs['tpID'])
            form.cleaned_data['trade_point'] = trade_point
            form.cleaned_data['status'] = QUEUE_STATUSES[0][0]
            return redirect('home', orgID=self.kwargs['orgID'],
                            tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data(**self.kwargs)
            context['form'] = form
            return render(request, template_name=self.template_name, context=context)

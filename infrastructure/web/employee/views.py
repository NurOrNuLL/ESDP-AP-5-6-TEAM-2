import json

from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

from models.employee.models import Employee
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointServices
from .forms import EmployeeForm
from services.employee_services import EmployeeServices
from .serializers import EmployeeSerializer
from .tasks import upload


class EmployeeCreate(TemplateView):
    template_name = 'employee/employee_create.html'
    form_class = EmployeeForm
    initial_data = {
        'role': 'Мастер'
    }

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponseRedirect or HttpResponse:
        context = self.get_context_data(**kwargs)
        context['tradepoints'] = EmployeeServices.get_tradepoint()

        context['roles'] = self.initial_data
        return render(request, self.template_name, context)

    def post(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            local_path = 'image/' + str(form.cleaned_data['image'])
            path = 'image/' + str(form.cleaned_data['image'])
            task = upload.apply_async(args=[local_path, path], ignore_result=True)
            EmployeeServices.create_employee(form.cleaned_data)
            return HttpResponse(
                json.dumps({"task_id": task.id}),
                content_type='application/json')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['roles'] = self.initial_data
            context['tradepoints'] = EmployeeServices.get_tradepoint()
            return render(request, self.template_name, context)


class EmployeeList(TemplateView):
    template_name = 'employee/employees.html'


class MyPagination(PageNumberPagination):
    page_size = 100


class EmployeeFilterApiView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'surname', 'IIN', 'phone']
    pagination_class = MyPagination

    def get_queryset(self):
        return Employee.objects.filter(tradepoint=self.kwargs.get('tpID'))


class EmployeeDetail(TemplateView):
    template_name = 'employee/employee_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['employee'] = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])
        return context

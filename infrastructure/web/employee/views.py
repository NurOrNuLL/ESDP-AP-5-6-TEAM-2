from datetime import datetime, date

from concurrency.api import disable_concurrency
from concurrency.exceptions import RecordModifiedError
from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django.core.files import File
from models.employee.models import Employee
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointServices
from .forms import EmployeeForm
from services.employee_services import EmployeeServices
from .serializers import EmployeeSerializer, EmployeeImageSerializer
from .tasks import upload
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class EmployeeCreate(ResetOrderCreateFormDataMixin, TemplateView):
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
        self.delete_order_data_from_session(request)
        context = self.get_context_data(**kwargs)
        context['tradepoints'] = EmployeeServices.get_tradepoint()

        context['roles'] = self.initial_data
        return render(request, self.template_name, context)

    def post(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            employee = EmployeeServices.create_employee_without_image(form.cleaned_data)
            return redirect(
                'employee_detail',
                orgID=self.kwargs['orgID'],
                tpID=self.kwargs['tpID'],
                empUID=employee.uuid
            )
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['roles'] = self.initial_data
            context['tradepoints'] = EmployeeServices.get_tradepoint()
            return render(request, self.template_name, context)


class EmployeeImageUpdateView(GenericAPIView):
    serializer_class = EmployeeImageSerializer

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        employee = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        task = upload.delay(serializer.data['image'], employee.uuid)

        return Response(
            {"task_id": task.id},
            content_type='application/json')


class EmployeeList(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'employee/employees.html'

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class MyPagination(PageNumberPagination):
    page_size = 100


class EmployeeFilterApiView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'surname', 'IIN', 'phone']
    pagination_class = MyPagination

    def get_queryset(self):
        return Employee.objects.filter(tradepoint=self.kwargs.get('tpID'))


class EmployeeDetail(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'employee/employee_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        employee = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['employee'] = employee
        context['empUID'] = employee.uuid
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class EmployeeUpdate(TemplateView):
    template_name = 'employee/employee_update.html'
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        self.object = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])
        context = super().get_context_data(**kwargs)
        context['employee'] = self.object
        context['tpID'] = self.kwargs['tpID']
        context['orgID'] = self.kwargs['orgID']
        context['tradepoints'] = EmployeeServices.get_tradepoint()
        context['roles'] = {'role': 'Мастер'}
        return context

    def get_file_form(self):
        form_kwargs = {'instance': EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return EmployeeForm(**form_kwargs)

    def get_inital(self, emp_uid: str) -> dict:
        employee = EmployeeServices.get_employee_by_uuid(emp_uid)
        initial = {
            'name': employee.name,
            'surname': employee.surname,
            'IIN': employee.IIN,
            'address': employee.address,
            'image': employee.image,
            'phone': employee.phone,
            'birthdate': employee.birthdate,
            'tradepoint': employee.tradepoint,
            'version': employee.version
        }
        return initial

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.get_file_form()
        context['image_remains'] = self.get_file_form()['image'].value()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        context['orgID'] = self.kwargs['orgID']
        self.request.session['image_remains'] = self.get_file_form()['image'].value().__str__()
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.object = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])
        context = self.get_context_data()
        form = self.get_file_form()
        if form.is_valid():
            try:
                form.save()
                EmployeeServices.update_employee(self.object.uuid, form.cleaned_data)
                return redirect('employee_detail', empUID=self.object.uuid, orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
            except RecordModifiedError:
                context['form'] = form.cleaned_data
                context['orgID'] = self.kwargs['orgID']
                context['tpID'] = self.kwargs['tpID']
                return render(request=request, template_name='employee/employee_update_conflict.html', context=context)
        else:
            context['form'] = form
            context['roles'] = {'role': 'Мастер'}
            context['tradepoints'] = EmployeeServices.get_tradepoint()
            context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
            context['orgID'] = self.kwargs['orgID']
            return render(request, self.template_name, context)


class EmployeeConcurrencyUpdate(View):
    def post(self, request, *args, **kwargs):
        employee = EmployeeServices.get_employee_by_uuid(self.kwargs['empUID'])
        with disable_concurrency(employee):
            employee.name = request.POST.get('name')
            employee.surname = request.POST.get('surname')
            employee.IIN = request.POST.get('IIN')
            employee.address = request.POST.get('address')
            employee.phone = request.POST.get('phone')
            employee.tradepoint = TradePointServices.get_trade_point_by_id(self.kwargs)
            employee.role = request.POST.get('role')
            employee.birthdate = request.POST.get('birthdate')
            employee.image = request.POST.get('image')
            employee.save()
            return redirect('employee_detail', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'],
                            empUID=self.kwargs['empUID'])


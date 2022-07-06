import ast
from typing import List

import jsonschema
from django.views.generic import TemplateView, View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from models.contractor.models import Contractor, MY_JSON_FIELD_SCHEMA
from services.employee_services import EmployeeServices
from services.own_services import OwnServices
from .forms import ContractorForm, ContractorUpdateForm
from django.shortcuts import render, redirect
from .serializers import ContractorSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from services.contractor_services import ContractorService
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointService
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from concurrency.exceptions import RecordModifiedError
from concurrency.api import disable_concurrency
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from ..own.serializer import OwnSerializer


class ContractorCreate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'contractor/contractor_create.html'
    form_class = ContractorForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        context = self.get_context_data(**kwargs)
        context['contractor_type'] = 'private'
        context['trust_person'] = dict()

        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)
        trust_person = dict(name=request.POST['trust_person_name'],
                            comment=request.POST['trust_person_comment'])
        try:
            jsonschema.validate(trust_person, MY_JSON_FIELD_SCHEMA)
        except jsonschema.exceptions.ValidationError:
            form.errors['trust_person'] = \
                'Не более 100 символов для Имени и не более 150 символов для Комментария для доверенного лица'

        if form.is_valid():
            form.cleaned_data['trust_person'] = trust_person
            contractor = ContractorService.create_contractor(form.cleaned_data)

            if request.GET.get('next'):
                request.session['contractor'] = contractor.id

                return redirect(request.GET.get('next'),
                                orgID=self.kwargs['orgID'],
                                tpID=self.kwargs['tpID'])
            else:
                return redirect('contractor_detail',
                            orgID=self.kwargs['orgID'],
                            contrID=contractor.pk, tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data(**kwargs)
            form.contractor_type = request.POST['contractor_type']
            context['contractor_type'] = form.contractor_type
            context['form'] = form
            context['trust_person'] = trust_person
            return render(request, template_name=self.template_name, context=context)


class ContractorList(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'contractor/contractors.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class MyPagination(PageNumberPagination):
    page_size = 100


class ContractorFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request: HttpRequest, queryset: List[Contractor], view: View) -> List[Contractor]:
        filtered_contractors = []
        for contractor in queryset:
            if (
                request.GET['search'].lower() in contractor.name.lower()
                or request.GET['search'].lower() in str(contractor.IIN_or_BIN)
                or request.GET['search'].lower() in str(contractor.phone)
            ):
                filtered_contractors.append(contractor)

        return filtered_contractors


class ContractorFilterApiView(generics.ListAPIView):
    serializer_class = ContractorSerializer
    filter_backends = [filters.OrderingFilter, ContractorFilterBackend]
    search_fields = ['IIN_or_BIN', 'phone']
    ordering_fields = ['name']
    pagination_class = MyPagination
    queryset = Contractor.objects.all()


class ContractorDetail(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'contractor/contractor_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['trade_point'] = TradePointService.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(
            self.kwargs['contrID']
        )
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)


class ContractorDetailOwnListApiView(generics.ListAPIView):
    serializer_class = OwnSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_part']
    pagination_class = MyPagination

    def get_object(self, **kwargs):
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        return contractor

    def get_queryset(self):
        return OwnServices.get_own_by_contr_id((self.get_object()).id)


class ContractorUpdate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'contractor/update.html'
    form_class = ContractorUpdateForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**self.kwargs)
        context['contractors'] = ContractorService.get_contractors(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        context['tpID'] = self.kwargs['tpID']
        context['orgID'] = self.kwargs['orgID']
        return context

    def get_inital(self, contr_id: int) -> dict:
        contractor = ContractorService.get_contractor_by_id(contr_id)
        initial = {
            'version': contractor.version,
            'name': contractor.name,
            'address': contractor.address,
            'IIC': contractor.IIC,
            'bank_name': contractor.bank_name,
            'BIC': contractor.BIC,
            'phone': contractor.phone,
        }
        return initial

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        form = self.form_class(initial=self.get_inital(contr_id=self.kwargs['contrID']))

        context = self.get_context_data()
        context['form'] = form
        context['trust_person'] = contractor.trust_person if contractor.trust_person else dict()
        context['tpID'] = TradePointService.get_tradepoint_id_from_cookie(self.request)
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict
             ) -> HttpResponse or HttpResponseRedirect:
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        context = self.get_context_data()
        form = self.form_class(data=request.POST, instance=contractor)
        trust_person = dict(name=request.POST['trust_person_name'],
                            comment=request.POST['trust_person_comment'])
        try:
            jsonschema.validate(trust_person, MY_JSON_FIELD_SCHEMA)
        except jsonschema.exceptions.ValidationError:
            form.errors['trust_person'] = \
                'Не более 100 символов для Имени и не более 150 символов для Комментария для доверенного лица'
        if form.is_valid():
            form.cleaned_data['trust_person'] = trust_person
            try:
                ContractorService.update_contractor(contractor, form.cleaned_data)
                return redirect('contractor_detail', orgID=1,
                                contrID=self.kwargs['contrID'], tpID=self.kwargs['tpID'])
            except RecordModifiedError:
                context['form'] = form.cleaned_data
                return render(request, template_name='contractor/contractor_update_compare.html', context=context)
        else:
            context['form'] = form
            context['trust_person'] = trust_person
            context['tpID'] = TradePointService.get_tradepoint_id_from_cookie(self.request)

            return render(request, template_name=self.template_name, context=context)


class ContractorUpdateConcurrecnyView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def post(self, request: HttpRequest, *args: list, **kwargs: dict
             ) -> HttpResponse or HttpResponseRedirect:
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])

        with disable_concurrency(contractor):
            contractor.name = request.POST.get('name')
            contractor.address = request.POST.get('address')
            contractor.IIN_or_BIN = request.POST.get('IIN_or_BIN')
            contractor.IIC = request.POST.get('IIC')
            contractor.BIC = request.POST.get('BIC')
            contractor.bank_name = request.POST.get('bank_name')
            contractor.phone = request.POST.get('phone')
            contractor.trust_person = ast.literal_eval(request.POST['trust_person'])
            contractor.save()
            return redirect('contractor_detail', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'],
                            contrID=self.kwargs['contrID'])

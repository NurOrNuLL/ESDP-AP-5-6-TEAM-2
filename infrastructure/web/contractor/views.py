from django.views.generic import TemplateView
from rest_framework import filters
from models.contractor.models import Contractor
from services.employee_services import EmployeeServices
from .forms import ContractorForm
from django.shortcuts import render, redirect
from .serializers import ContractorSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from services.contractor_services import ContractorService
from services.organization_services import OrganizationService
from services.trade_point_services import TradePointServices
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect


class ContractorCreate(TemplateView):
    template_name = 'contractor/contractor_create.html'
    form_class = ContractorForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        context['trust_person'] = dict()

        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)
        if form.is_valid():
            trust_person = dict(name=request.POST['trust_person_name'],
                                comment=request.POST['trust_person_comment'])
            form.cleaned_data['trust_person'] = trust_person
            contractor = ContractorService.create_contractor(form.cleaned_data)
            return redirect('contractor_detail',
                            orgID=self.kwargs['orgID'], contrID=contractor.pk, tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['trust_person'] = dict(name=request.POST['trust_person_name'],
                                           comment=request.POST['trust_person_comment'])
            return render(request, template_name=self.template_name, context=context)


class ContractorList(TemplateView):
    template_name = 'contractor/contractors.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(kwargs)
        context['tpID'] = self.kwargs['tpID']
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        return context


class MyPagination(PageNumberPagination):
    page_size = 100


class ContractorFilterApiView(generics.ListAPIView):
    serializer_class = ContractorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'IIN_or_BIN', 'phone']
    pagination_class = MyPagination
    queryset = Contractor.objects.all()


class ContractorDetail(TemplateView):
    template_name = 'contractor/contractor_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        context['trade_point'] = TradePointServices.get_trade_point_by_id(self.kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        return context


class ContractorUpdate(TemplateView):
    template_name = 'contractor/update.html'
    form_class = ContractorForm

    def get_inital(self, contr_id: int) -> dict:
        contractor = ContractorService.get_contractor_by_id(contr_id)
        initial = {
            'name': contractor.name,
            'address': contractor.address,
            'IIN_or_BIN': contractor.IIN_or_BIN,
            'IIC': contractor.IIC,
            'bank_name': contractor.bank_name,
            'BIC': contractor.BIC,
            'phone': contractor.phone,
        }

        return initial

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        form = self.form_class(initial=self.get_inital(contr_id=self.kwargs['contrID']), instance=contractor)

        context = self.get_context_data()
        context['form'] = form
        context['trust_person'] = contractor.trust_person if contractor.trust_person else dict()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        form = self.form_class(data=request.POST, instance=contractor)

        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'address': form.cleaned_data['address'],
                'IIN_or_BIN': form.cleaned_data['IIN_or_BIN'],
                'IIC': form.cleaned_data['IIC'],
                'bank_name': form.cleaned_data['bank_name'],
                'BIC': form.cleaned_data['BIC'],
                'phone': form.cleaned_data['phone'],
                'trust_person_name': request.POST['trust_person_name'],
                'trust_person_comment': request.POST['trust_person_comment']
            }

            ContractorService.update_contractor(contractor, data)

            return redirect('contractor_detail', orgID=1, contrID=self.kwargs['contrID'], tpID=self.kwargs['tpID'])
        else:
            context = self.get_context_data()
            context['form'] = form
            context['trust_person'] = dict(name=request.POST['trust_person_name'],
                                           comment=request.POST['trust_person_comment'])

            return render(request, template_name=self.template_name, context=context)

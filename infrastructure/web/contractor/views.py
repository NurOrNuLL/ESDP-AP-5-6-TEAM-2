import json
from django.views.generic import TemplateView
from models.contractor.models import Contractor
from .forms import ContractorForm
from django.shortcuts import render, redirect
from services.contractor_services import ContractorService
from services.organization_services import OrganizationService
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

class ContractorCreate(TemplateView):
    template_name = 'contractor/contractor_create.html'
    form_class = ContractorForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            trust_person = dict(name=request.POST['trust_person_name'],
                                comment=request.POST['trust_person_comment'])
            form.cleaned_data['trust_person'] = trust_person
            contractor = ContractorService.create_contractor(form.cleaned_data)
            return redirect('contractor_detail',
                            orgID=self.kwargs['orgID'], contrID=contractor.pk)
        return render(request, self.template_name, {'form': form})


class ContractorList(TemplateView):
    template_name = 'contractor/contractors.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['contractors'] = ContractorService.get_contractors(kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        return context


class ContractorDetail(TemplateView):
    template_name = 'contractor/contractor_detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['contractor'] = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
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

        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        contractor = ContractorService.get_contractor_by_id(self.kwargs['contrID'])
        form = self.form_class(data=request.POST, instance=contractor)

        if form.is_valid():
            ContractorService.update_contractor(contractor, request, form)

            return redirect('contractor_detail', orgID=1, contrID=self.kwargs['contrID'])
        else:
            context = self.get_context_data()
            context['form'] = form
            context['trust_person'] = dict(name=request.POST['trust_person_name'],
                                           comment=request.POST['trust_person_comment'])

            return render(request, template_name=self.template_name, context=context)

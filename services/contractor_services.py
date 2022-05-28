from models.contractor.models import Contractor
from models.organization.models import Organization
from typing import List
from django.http.request import HttpRequest
from django.forms import ModelForm


class ContractorService:
    @staticmethod
    def create_contractor(data: dict) -> Contractor:
        return Contractor.objects.create(
            name=data['name'],
            address=data['address'],
            IIN_or_BIN=data['IIN_or_BIN'],
            bank_requisition=data['bank_requisition'],
            phone=data['phone'],
            trust_person=data['trust_person'],
            organization=Organization.objects.get(id=1),
        )

    @staticmethod
    def update_contractor(contractor: Contractor, request: HttpRequest, form: ModelForm) -> None:
        trust_person = dict(name=request.POST['trust_person_name'],
                            comment=request.POST['trust_person_comment'])

        contractor.name = form.cleaned_data['name']
        contractor.address = form.cleaned_data['address']
        contractor.IIN_or_BIN = form.cleaned_data['IIN_or_BIN']
        contractor.IIC = form.cleaned_data['IIC']
        contractor.bank_name = form.cleaned_data['bank_name']
        contractor.BIC = form.cleaned_data['BIC']
        contractor.phone = form.cleaned_data['phone']
        contractor.trust_person = trust_person
        contractor.save()

    @staticmethod
    def get_contractors(kwargs: dict) -> List['Contractor']:
        return Contractor.objects.filter(organization=kwargs['orgID'])

    @staticmethod
    def get_contractor_by_id(contr_id: int) -> Contractor:
        return Contractor.objects.get(id=contr_id)

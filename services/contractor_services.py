from models.contractor.models import Contractor
from models.organization.models import Organization
from django.shortcuts import get_object_or_404


def create_contractor(data):
    return Contractor.objects.create(
        name=data['name'],
        address=data['address'],
        IIN_or_BIN=data['IIN_or_BIN'],
        IIC=data['IIC'],
        bank_name=data['bank_name'],
        BIC=data['BIC'],
        phone=data['phone'],
        trust_person=data['trust_person'],
        organization=get_object_or_404(Organization, id=1),
    )


def get_contractors(kwargs):
    return Contractor.objects.filter(organization=kwargs['orgID'])


def get_contractor_by_id(kwargs):
    return get_object_or_404(Contractor, id=kwargs['contrID'])

from models.contractor.models import Contractor
from models.organization.models import Organization
from typing import List


class ContractorService:
    @staticmethod
    def create_contractor(data: dict) -> Contractor:
        return Contractor.objects.create(
            name=data['name'],
            address=data['address'],
            IIN_or_BIN=data['IIN_or_BIN'],
            IIC=data['IIC'],
            bank_name=data['bank_name'],
            BIC=data['BIC'],
            phone=data['phone'],
            trust_person=data['trust_person'],
            organization=Organization.objects.get(id=1),
        )

    @staticmethod
    def update_contractor(contractor: Contractor, data: dict) -> None:
        contractor.name = data['name']
        contractor.address = data['address']
        contractor.IIN_or_BIN = data['IIN_or_BIN']
        contractor.IIC = data['IIC']
        contractor.bank_name = data['bank_name']
        contractor.BIC = data['BIC']
        contractor.phone = data['phone']
        contractor.trust_person = {
            'name': data['trust_person_name'],
            'comment': data['trust_person_comment']
        }

        contractor.save()

        return contractor

    @staticmethod
    def get_contractors(kwargs: dict) -> List['Contractor']:
        return Contractor.objects.filter(organization=kwargs['orgID'])

    @staticmethod
    def get_contractor_by_id(contrID: int) -> Contractor:
        return Contractor.objects.get(id=contrID)

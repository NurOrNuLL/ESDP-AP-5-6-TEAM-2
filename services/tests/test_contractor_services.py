from unittest import TestCase
from models.contractor.models import Contractor
from models.organization.models import Organization
from services.contractor_services import ContractorService
from unittest.mock import Mock, patch


class ContractorServicesTest(TestCase):
    def test_get_contractor_by_id(self):
        contractor = Mock(spec=Contractor, id=1)

        with patch('models.contractor.models.Contractor.objects.get') as get_contrator:
            get_contrator.return_value = contractor

            returned_contractor = ContractorService.get_contractor_by_id(
                contrID=contractor.id
            )

            self.assertEqual(returned_contractor, contractor)
            get_contrator.assert_called_once_with(id=contractor.id)

    def test_get_contractors(self):
        organization = Mock(spec=Organization, id=1)

        contractors = [Mock(spec=Contractor, id=1), Mock(spec=Contractor, id=2)]

        with patch('models.contractor.models.Contractor.objects.filter') as \
                filter_contractor:
            filter_contractor.return_value = contractors

            returned_contractors = ContractorService.get_contractors(
                {'orgID': organization.id}
            )

            self.assertListEqual(returned_contractors, contractors)
            filter_contractor.assert_called_once_with(organization=organization.id)

    def test_update_contractor(self):
        contractor = Mock(
            spec=Contractor,
            name='Данил',
            address='Какой-то адрес',
            IIN_or_BIN=123123123123,
            IIC='',
            bank_name='',
            BIC='',
            phone='+77777777777',
            trust_person={
                'name': '',
                'comment': ''
            }
        )

        data = {
            'name': 'Данилaaaaaaaaa',  # noqa E126
            'address': 'Новый адрес',
            'IIN_or_BIN': 111111111111,
            'IIC': contractor.IIC,
            'bank_name': contractor.bank_name,
            'BIC': contractor.BIC,
            'phone': '87772755701',
            'trust_person': {'name': 'чоо', 'comment': 'ыва'}
        }

        with patch('models.contractor.models.Contractor.save') as save_contractor:
            save_contractor.return_value = None

            returned_contractor = ContractorService.update_contractor(contractor, data)

            self.assertDictEqual(data, {
                'name': returned_contractor.name,
                'address': returned_contractor.address,
                'IIN_or_BIN': returned_contractor.IIN_or_BIN,
                'IIC': returned_contractor.IIC,
                'bank_name': returned_contractor.bank_name,
                'BIC': returned_contractor.BIC,
                'phone': returned_contractor.phone,
                'trust_person': returned_contractor.trust_person,
            })

    def test_create_contractor(self):
        organization = Mock(spec=Organization, id=1)
        queryset = [Mock(spec=Contractor)]
        data = {
            'name': 'Данилaaaaaaaaa',
            'address': '',
            'IIN_or_BIN': 111111111111,
            'IIC': '',
            'bank_name': '',
            'BIC': '',
            'phone': '88888888888',
            'trust_person': {
                'name': 'чоо',
                'comment': 'йомайо'
            },
        }

        with patch('models.contractor.models.Contractor.objects.create') as \
                create_contractor:
            with patch('models.organization.models.Organization.objects.get') as \
                    get_organization:
                create_contractor.return_value = Mock(
                    spec=Contractor,
                    name=data['name'],
                    address=data['address'],
                    IIN_or_BIN=data['IIN_or_BIN'],
                    IIC=data['IIC'],
                    bank_name=data['bank_name'],
                    BIC=data['BIC'],
                    phone=data['phone'],
                    trust_person=data['trust_person'],
                    organization=organization
                )

                get_organization.return_value = organization

                contractor = ContractorService.create_contractor(data)
                queryset.append(contractor)

                self.assertIn(contractor, queryset)
                create_contractor.assert_called_once_with(
                    name=data['name'],
                    address=data['address'],
                    IIN_or_BIN=data['IIN_or_BIN'],
                    IIC=data['IIC'],
                    bank_name=data['bank_name'],
                    BIC=data['BIC'],
                    phone=data['phone'],
                    trust_person=data['trust_person'],
                    organization=organization
                )
                get_organization.assert_called_once_with(id=organization.id)

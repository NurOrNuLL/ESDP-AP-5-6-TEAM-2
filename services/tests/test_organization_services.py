from django.test import TestCase
from models.organization.models import Organization
from services.organization_services import OrganizationService


class OrganizationServicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name='Тестовая организация',
            address='Тестовый адрес',
            RNN='112233445566',
            BIN='998877445566',
            bank_requisition='Тестовые реквизиты'
        )

    def test_get_organization_by_id(self):
        organization = OrganizationService.get_organization_by_id({"orgID": self.organization.id})
        self.assertEqual(organization, self.organization)

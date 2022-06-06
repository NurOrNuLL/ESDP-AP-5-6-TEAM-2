from unittest import TestCase
from unittest.mock import Mock, patch
from models.organization.models import Organization
from services.organization_services import OrganizationService


class OrganizationServicesTest(TestCase):
    def test_get_organization_by_id(self):
        organization = Mock(spec=Organization, id=1)

        with patch('models.organization.models.Organization.objects.get') as get_organization:
            get_organization.return_value = organization

            returned_organization = OrganizationService.get_organization_by_id(kwargs={"orgID": organization.id})
            self.assertEqual(returned_organization, organization)
            get_organization.assert_called_once_with(id=organization.id)

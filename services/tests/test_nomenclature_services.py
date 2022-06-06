from unittest import TestCase
from models.nomenclature.models import Nomenclature
from services.nomenclature_services import NomenclatureService
from unittest.mock import Mock, patch
from models.organization.models import Organization


class NomenclatureServicesTest(TestCase):
    def test_get_nomenclature_by_id(self):
        nomenclature = Mock(spec=Nomenclature, id=1)

        with patch('models.nomenclature.models.Nomenclature.objects.get') as get_nomenclature:
            get_nomenclature.return_value = nomenclature

            returned_nomenclature = NomenclatureService.get_nomenclature_by_id(nomenclature_id=nomenclature.id)

            self.assertEqual(returned_nomenclature, nomenclature)
            get_nomenclature.assert_called_once_with(id=nomenclature.id)

    def test_create_nomenclature(self):
        organization = Mock(spec=Organization, id=1)
        queryset = [Mock(spec=Nomenclature)]
        data = {
                'name': 'СТО',
        }

        with patch('models.nomenclature.models.Nomenclature.objects.create') as create_nomenclature:
            with patch('models.organization.models.Organization.objects.get') as get_organization:
                create_nomenclature.return_value = Mock(
                    spec=Nomenclature,
                    name=data['name'],
                    organization=organization
                )

                get_organization.return_value = organization

                nomenclature = NomenclatureService.create_nomenclature(data)
                queryset.append(nomenclature)
                self.assertIn(nomenclature, queryset)
                create_nomenclature.assert_called_once_with(
                    name=data['name'],
                    organization=organization
                )
                get_organization.assert_called_once_with(id=organization.id)
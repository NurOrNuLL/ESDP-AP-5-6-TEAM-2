from unittest import TestCase
from models.nomenclature.models import Nomenclature
from services.nomenclature_services import NomenclatureService
from unittest.mock import Mock, patch


class NomenclatureServicesTest(TestCase):
    def test_get_nomenclature_by_id(self):
        nomenclature = Mock(spec=Nomenclature, id=1)

        with patch('models.nomenclature.models.Nomenclature.objects.get') as get_nomenclature:
            get_nomenclature.return_value = nomenclature

            returned_nomenclature = NomenclatureService.get_nomenclature_by_id(nomenclature_id=nomenclature.id)

            self.assertEqual(returned_nomenclature, nomenclature)
            get_nomenclature.assert_called_once_with(id=nomenclature.id)
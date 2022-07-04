import json
from django.test import SimpleTestCase, Client
from unittest.mock import Mock, patch

from django.urls import reverse
from models.organization.models import Organization
from models.trade_point.models import TradePoint
from models.nomenclature.models import Nomenclature
from concurrency.exceptions import RecordModifiedError


class NomenclatureUpdateViewTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client(enforce_csrf_checks=False, raise_request_exception=False)
        cls.organization = Mock(spec=Organization, id=1)
        cls.tradepoint = Mock(spec=TradePoint, id=1)

        nomenclature = Mock(spec=Nomenclature, id=1, version=0)
        nomenclature.name = 'Тестовая номенклатура'

        cls.nomenclature = nomenclature

    def test_nomenclature_update_GET(self) -> AssertionError or None:
        path_GET = reverse(
            'nomenclature_update',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'pk': self.nomenclature.id
            }
        )

        due_resp = {
            'name': self.nomenclature.name,
            'version': self.nomenclature.version
        }

        with patch('services.nomenclature_services.NomenclatureService.get_nomenclature_by_id') as get_nomenclature_by_id:
            get_nomenclature_by_id.return_value = self.nomenclature

            resp_GET = self.client.get(path=path_GET)

            self.assertDictEqual(resp_GET.json(), due_resp)
            get_nomenclature_by_id.assert_called_once_with(self.nomenclature.id)

    def test_nomenclature_update_PATCH(self) -> AssertionError or None:
        path_PATCH = reverse(
            'nomenclature_update',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'pk': self.nomenclature.id
            }
        )

        data_PATCH = {
            'version': self.nomenclature.version,
            'name': 'Новое название'
        }

        due_resp = {
            'version': self.nomenclature.version + 1,
            'name': 'Новое название'
        }

        with patch('services.nomenclature_services.NomenclatureService.get_nomenclature_by_id') as get_nomenclature_by_id:
            with patch('infrastructure.web.nomenclature.serializers.NomenclatureUpdateSerializer.is_valid') as is_valid:
                with patch('infrastructure.web.nomenclature.serializers.NomenclatureUpdateSerializer.save') as save:
                    with patch('infrastructure.web.nomenclature.serializers.NomenclatureUpdateSerializer.data', {'version': self.nomenclature.version + 1, 'name': 'Новое название'}):
                        def save_nomenclature() -> None:
                            self.nomenclature.version += 1
                            self.nomenclature.name = data_PATCH['name']

                        is_valid.return_value = True
                        save.side_effect = save_nomenclature

                        get_nomenclature_by_id.return_value = self.nomenclature

                        resp_PATCH = self.client.patch(path_PATCH, data=data_PATCH, content_type='application/json')

                        self.assertDictEqual(resp_PATCH.json(), due_resp)
                        is_valid.assert_called_once()
                        save.assert_called_once()
                        get_nomenclature_by_id.assert_called_once_with(self.nomenclature.id)

    def test_nomenclature_update_concurrency_PATCH(self) -> AssertionError or None:
        path_PATCH = reverse(
            'nomenclature_update',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'pk': self.nomenclature.id
            }
        )

        data_PATCH = {
            'version': self.nomenclature.version,
            'name': 'Новое название'
        }

        due_resp = {
            'current_data': {'name': self.nomenclature.name},
            'new_data': {'name': self.nomenclature.name},
            'error': 'Наименование номенклатуры было изменено другим пользователем! Вы хотите повторно изменить наименование?'
        }

        with patch('services.nomenclature_services.NomenclatureService.get_nomenclature_by_id') as get_nomenclature_by_id:
            with patch('infrastructure.web.nomenclature.serializers.NomenclatureUpdateSerializer.is_valid') as is_valid:
                with patch('infrastructure.web.nomenclature.serializers.NomenclatureUpdateSerializer.save') as save:
                    def raise_exception() -> RecordModifiedError:
                        raise RecordModifiedError(target=None)

                    is_valid.return_value = True
                    save.side_effect = raise_exception

                    get_nomenclature_by_id.return_value = self.nomenclature

                    resp_PATCH = self.client.patch(path_PATCH, data=data_PATCH, content_type='application/json')

                    self.assertDictEqual(resp_PATCH.json(), due_resp)
                    is_valid.assert_called_once()
                    save.assert_called_once()
                    get_nomenclature_by_id.assert_called_with(self.nomenclature.id)

    def test_concurrency_update_nomenclature_view(self) -> AssertionError or None:
        path_PATCH = reverse(
            'nomenclature_update_concurrency',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'pk': self.nomenclature.id
            }
        )

        data_PATCH = {
            'name': 'Новое название2'
        }

        due_resp = {
            'name': 'Новое название2',
            'version': self.nomenclature.version
        }

        with patch('services.nomenclature_services.NomenclatureService.get_nomenclature_by_id') as get_nomenclature_by_id:
            with patch('models.nomenclature.models.Nomenclature.save') as save:
                get_nomenclature_by_id.return_value = self.nomenclature

                def save_nomenclature() -> None:
                    self.nomenclature.name = data_PATCH['name']

                save.side_effect = save_nomenclature

                resp_PATCH = self.client.patch(path_PATCH, data_PATCH, content_type='application/json')

                self.assertDictEqual(resp_PATCH.json(), due_resp)
                get_nomenclature_by_id.assert_called_once_with(self.nomenclature.id)

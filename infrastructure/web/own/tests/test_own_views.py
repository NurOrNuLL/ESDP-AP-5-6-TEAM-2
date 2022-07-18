import json
from django.test import SimpleTestCase, Client
from unittest.mock import Mock, patch

from django.urls import reverse
from models.organization.models import Organization
from models.trade_point.models import TradePoint
from models.own.models import Own
from concurrency.exceptions import RecordModifiedError


class OwnUpdateViewTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client(enforce_csrf_checks=False, raise_request_exception=False)
        cls.organization = Mock(spec=Organization, id=1)
        cls.tradepoint = Mock(spec=TradePoint, id=1)

        own = Mock(spec=Own, id=1, version=0)
        own.name = 'Новое название'
        own.number = 'Новый номер'
        own.comment = 'Новый коментарий'

        cls.own = own

    def test_own_update_PATCH(self) -> AssertionError or None:
        path_PATCH = reverse(
            'own_update',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'ownID': self.own.id
            }
        )

        data_PATCH = {
            'version': self.own.version,
            'name': 'Новое название',
            'number': 'Новый номер',
            'comment': 'Новый коментарий'
        }

        due_resp = {
            'version': self.own.version + 1,
            'name': 'Новое название',
            'number': 'Новый номер',
            'comment': 'Новый коментарий'
        }

        with patch('services.own_services.OwnServices.get_own_by_id') as get_own_by_id:
            with patch('infrastructure.web.own.serializer.OwnUpdateSerializer.is_valid') as is_valid:
                with patch('infrastructure.web.own.serializer.OwnUpdateSerializer.save') as save:
                    with patch('infrastructure.web.own.serializer.OwnUpdateSerializer.data', {'version': self.own.version + 1, 'name': 'Новое название', 'number': 'Новый номер', 'comment': 'Новый коментарий'}):
                        def save_own() -> None:
                            self.own.version += 1
                            self.own.name = data_PATCH['name']
                            self.own.number = data_PATCH['number']
                            self.own.comment = data_PATCH['comment']

                        is_valid.return_value = True
                        save.side_effect = save_own

                        get_own_by_id.return_value = self.own

                        resp_PATCH = self.client.patch(path_PATCH, data=data_PATCH, content_type='application/json')

                        self.assertDictEqual(resp_PATCH.json(), due_resp)
                        is_valid.assert_called_once()
                        save.assert_called_once()
                        get_own_by_id.assert_called_once_with(self.own.id)

    def test_own_update_concurrency_PATCH(self) -> AssertionError or None:
        path_PATCH = reverse(
            'own_update',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'ownID': self.own.id
            }
        )

        data_PATCH = {
            'version': self.own.version,
            'name': 'Новое название',
            'number': 'НОВЫЙ НОМЕР',
            'comment': 'Новый коментарий'
        }

        due_resp = {
            'current_data': {'name': self.own.name, 'number': self.own.number, 'comment': self.own.comment},
            'new_data': {'name': self.own.name, 'number': self.own.number, 'comment': self.own.comment},
            'error': 'Наименование собственности было изменено другим пользователем! Вы хотите повторно изменить наименование?'
        }

        with patch('services.own_services.OwnServices.get_own_by_id') as get_own_by_id:
            with patch('infrastructure.web.own.serializer.OwnUpdateSerializer.is_valid') as is_valid:
                with patch('infrastructure.web.own.serializer.OwnUpdateSerializer.save') as save:
                    def raise_exception() -> RecordModifiedError:
                        raise RecordModifiedError(target=None)

                    is_valid.return_value = True
                    save.side_effect = raise_exception

                    get_own_by_id.return_value = self.own

                    resp_PATCH = self.client.patch(path_PATCH, data=data_PATCH, content_type='application/json')

                    self.assertDictEqual(resp_PATCH.json(), due_resp)
                    is_valid.assert_called_once()
                    save.assert_called_once()
                    get_own_by_id.assert_called_with(self.own.id)

    def test_concurrency_update_own_view(self) -> AssertionError or None:
        path_PATCH = reverse(
            'own_update_concurrency',
            kwargs={
                'orgID': self.organization.id,
                'tpID': self.tradepoint.id,
                'ownID': self.own.id
            }
        )

        data_PATCH = {
            'name': 'Новое название2',
            'number': 'Новый номер2',
            'comment': 'Новый коментарий2',
            'version': self.own.version
        }

        due_resp = {
            'name': 'Новое название2',
            'number': 'Новый номер2',
            'comment': 'Новый коментарий2',
            'version': self.own.version
        }

        with patch('services.own_services.OwnServices.get_own_by_id') as get_own_by_id:
            with patch('models.own.models.Own.save') as save:
                get_own_by_id.return_value = self.own

                def save_own() -> None:
                    self.own.name = data_PATCH['name']
                    self.own.number = data_PATCH['number']
                    self.own.comment = data_PATCH['comment']

                save.side_effect = save_own

                resp_PATCH = self.client.patch(path_PATCH, data_PATCH, content_type='application/json')

                self.assertDictEqual(resp_PATCH.json(), due_resp)
                get_own_by_id.assert_called_once_with(self.own.id)

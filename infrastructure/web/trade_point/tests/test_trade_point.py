from unittest import TestCase

from models.nomenclature.models import Nomenclature
from models.trade_point.models import TradePoint
from services.trade_point_services import TradePointServices
from unittest.mock import Mock, patch
from concurrency.exceptions import RecordModifiedError


class TradePointTest(TestCase):
    def test_update_trade_point(self):
        nomenclature = Mock(spec=Nomenclature, id=1)

        trade_point = Mock(spec=TradePoint, version=1, name='Филиал',
                           address='Какой-то адрес', nomenclature=nomenclature
                           )

        with patch('models.nomenclature.models.nomenclature.objects.get') as get_nomenclature:
            get_nomenclature.return_value = nomenclature
            with patch('models.trade_point.models.TradePoint.save') as save_trade_point:
                save_trade_point.return_value = None

                def save():
                    trade_point.version += 1

                trade_point.save = save

                data = {
                    'name': 'Филиал 1',
                    'address': 'Новый адрес',
                    'nomenclature': trade_point.nomenclature
                }

                returned_trade_point_version = TradePointServices.update_trade_point(trade_point, data).version

                trade_point.save()
                with self.assertRaises(RecordModifiedError):
                    if trade_point.version != returned_trade_point_version:
                        raise RecordModifiedError(target=trade_point)

from typing import List
from unittest import TestCase

from models.nomenclature.models import Nomenclature
from models.trade_point.models import TradePoint
from services.trade_point_services import TradePointServices
from unittest.mock import Mock, patch
from concurrency.exceptions import RecordModifiedError


class TradePointTest(TestCase):
    def test_update_trade_point(self):
        nomenclature1 = Mock(spec=Nomenclature, id=1)
        nomenclature2 = Mock(spec=Nomenclature, id=2)
        mock_queryset = Mock(nomenclatures=[nomenclature2, nomenclature1])

        with patch('models.trade_point.models.TradePoint.save') as save_trade_point:
            save_trade_point.return_value = None

            trade_point = Mock(
                spec=TradePoint, version=1,
                name='Филиал', address='Какой-то адрес',
                nomenclature=mock_queryset
            )

            def save():
                trade_point.version += 1

            trade_point.save_trade_point = save

            def set(nomenclatures: List[Nomenclature]) -> None:
                trade_point.nomenclature = nomenclatures

            trade_point.nomenclature.set = set

            data = {
                'name': 'Филиал 1',
                'address': 'Новый адрес',
                'nomenclature': [nomenclature1]
            }

            returned_trade_point_version = TradePointServices.update_trade_point(trade_point, data).version

            trade_point.save_trade_point()
            with self.assertRaises(RecordModifiedError):
                if trade_point.version != returned_trade_point_version:
                    raise RecordModifiedError(target=trade_point)

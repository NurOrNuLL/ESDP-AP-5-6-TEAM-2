from unittest import TestCase
from models.trade_point.models import TradePoint
from services.trade_point_services import TradePointServices
from unittest.mock import Mock, patch


class TradePointServicesTest(TestCase):
    def test_get_trade_point_by_id(self):
        trade_point = Mock(spec=TradePoint, id=1)

        with patch('models.trade_point.models.TradePoint.objects.get') as get_trade_point:
            get_trade_point.return_value = trade_point

            returned_trade_point = TradePointServices.get_trade_point_by_id(
                kwargs={"tpID": trade_point.id}
            )

            self.assertEqual(returned_trade_point, trade_point)
            get_trade_point.assert_called_once_with(id=trade_point.id)

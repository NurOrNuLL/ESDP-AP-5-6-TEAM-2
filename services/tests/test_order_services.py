from unittest import TestCase
from models.order.models import Order
from models.trade_point.models import TradePoint
from models.contractor.models import Contractor
from models.own.models import Own
from models.payment.models import Payment
from services.order_services import OrderService
from unittest.mock import Mock, patch


class OrderServicesTest(TestCase):
    def test_get_order_by_id(self):
        order = Mock(spec=Order, id=1)

        with patch('models.order.models.Order.objects.get') as get_order:
            get_order.return_value = order

            returned_order = OrderService.get_order_by_id(ordID=order.id)

            self.assertEqual(returned_order, order)
            get_order.assert_called_once_with(id=order.id)


    def test_get_orders_by_trade_point(self):
        trade_point = Mock(spec=TradePoint, id=1)
        orders = [Mock(spec=Order, id=1), Mock(spec=Order, id=2)]

        with patch('models.order.models.Order.objects.filter') as filter_orders:
            filter_orders.return_value = orders

            returned_orders = OrderService.get_orders_by_trade_point({'tpID': trade_point.id})

            self.assertListEqual(returned_orders, orders)
            filter_orders.assert_called_once_with(trade_point=trade_point.id)

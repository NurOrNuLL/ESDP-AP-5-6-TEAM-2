from unittest import TestCase
from models.order.models import Order
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

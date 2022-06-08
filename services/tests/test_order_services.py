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


    def test_create_order(self):
        trade_point = Mock(spec=TradePoint, id=1)
        contractor = Mock(spec=Contractor, id=1)
        own = Mock(spec=Own, id=1)
        payment = Mock(spec=Payment, id=1)
        queryset = [Mock(spec=Order)]
        data = {
            'trade_point': trade_point.id,
            'contractor': contractor.id,
            'own': own.id,
            'payment': payment.id,
            'finished_at': '',
            'status': 'В работе',
            'price': 100,
            'note': '',
            'mileage': 1000,
            'jobs': {
                'Заказ': 1,
                'Название услуги': 'Какая-то услуга',
                'Цена услуги': 100,
                'Гарантия': False,
                'Мастера': [1, 2],
            },
        }

        with patch('models.order.models.Order.objects.create') as create_order:
            with patch('models.trade_point.models.TradePoint.objects.get') as get_trade_point:
                with patch('models.contractor.models.Contractor.objects.get') as get_contractor:
                    with patch('models.own.models.Own.objects.get') as get_own:
                        with patch('models.payment.models.Payment.objects.get') as get_payment:

                            create_order.return_value = Mock(
                                spec=Order,
                                finished_at=data['finished_at'],
                                status=data['status'],
                                price=data['price'],
                                note=data['note'],
                                mileage=data['mileage'],
                                jobs=data['jobs'],
                                trade_point=data['trade_point'],
                                contractor=data['contractor'],
                                own=data['own'],
                                payment=data['payment'],
                            )

                            trade_point.return_value = trade_point
                            contractor.return_value = contractor
                            own.return_value = own
                            payment.return_value = payment

                            order = OrderService.create_order(data)
                            queryset.append(order)

                            self.assertIn(order, queryset)
                            create_order.assert_called_once_with(
                                finished_at=data['finished_at'],
                                status=data['status'],
                                price=data['price'],
                                note=data['note'],
                                mileage=data['mileage'],
                                jobs=data['jobs'],
                                trade_point=data['trade_point'],
                                contractor=data['contractor'],
                                own=data['own'],
                                payment=data['payment'],
                            )

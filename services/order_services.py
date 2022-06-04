from models.order.models import Order
from typing import List


class OrderService:
    @staticmethod
    def create_order(data: dict) -> Order:
        return Order.objects.create(
            trade_point=data['trade_point'],
            contractor=data['contractor'],
            own=data['own'],
            finished_at=data['finished_at'],
            status=data['status'],
            price=data['price'],
            payment=data['payment'],
            note=data['note'],
            mileage=data['mileage'],
        )

    @staticmethod
    def get_orders_by_trade_point(kwargs: dict) -> List['Order']:
        return Order.objects.filter(trade_point=kwargs['tpID'])

    @staticmethod
    def get_order_by_id(ord_id: int) -> Order:
        return Order.objects.get(id=ord_id)

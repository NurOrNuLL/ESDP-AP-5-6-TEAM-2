from models.order.models import Order
from typing import List


class OrderService:
    @staticmethod
    def create_order(data: dict) -> Order:
        return Order.objects.create(
            trade_point=data['trade_point'],
            contractor=data['contractor'],
            own=data['own'],
            status=data['status'],
            price_for_pay=data['price_for_pay'],
            full_price=data['full_price'],
            payment=data['payment'],
            note=data['note'],
            mileage=data['mileage'],
            jobs=data['jobs'],
        )

    @staticmethod
    def get_orders_by_trade_point(kwargs: dict) -> List['Order']:
        return Order.objects.filter(trade_point=kwargs['tpID'])

    @staticmethod
    def get_order_by_id(ordID: int) -> Order:
        return Order.objects.get(id=ordID)

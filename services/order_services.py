import datetime
from models.order.models import Order
from typing import Any, Dict, List
from services.trade_point_services import TradePointServices
import pytz


utc = pytz.UTC


class OrderService:
    @staticmethod
    def get_finished_orders_in_period(from_date: datetime.date, to_date: datetime.date, tpID: int) -> List[Order]:
        trade_point = TradePointServices.get_trade_point_by_clean_id(tpID)
        all_orders = Order.objects.filter(trade_point=trade_point, status='Завершен')

        orders = [order for order in all_orders \
                    if order.finished_at >= utc.localize(from_date) \
                    and order.finished_at <= utc.localize(to_date)]

        return orders

    @staticmethod
    def create_order(data: dict) -> Order:
        return Order.objects.create(
            trade_point=data['trade_point'],
            contractor=data['contractor'],
            nomenclature=data['nomenclature'],
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
    def get_initial_for_update(order: Order) -> Dict[str, Any]:
        return {
            'jobs': order.jobs,
            'mileage': order.mileage,
            'note': order.note,
            'version': order.version
        }

    @staticmethod
    def get_orders_by_trade_point(kwargs: dict) -> List['Order']:
        return Order.objects.filter(trade_point=kwargs['tpID'])

    @staticmethod
    def get_order_by_id(ordID: int) -> Order:
        return Order.objects.get(id=ordID)

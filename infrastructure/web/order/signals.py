import datetime
import json
from models.order.models import Order
from models.payment.models import Payment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OrderDataclass:
    id: int
    status: Optional[str] = 'В работе'

@dataclass
class PaymentDataclass:
    status: str
    order_id: Optional[int] = None


def get_old_order_status(sender: Order, instance: Order, **kwargs: Any) -> None:
    OrderDataclass.id = instance.id

def get_new_order_status(sender: Order, instance: Order, **kwargs: Any) -> None:
    channel_layer = get_channel_layer()

    if OrderDataclass.status != instance.status:
        async_to_sync(channel_layer.group_send)(
            'orderStatuses',
            {
                'type': 'update_status',
                'id': OrderDataclass.id,
                'status': instance.status,
                'finished_at': instance.finished_at.strftime('%Y-%m-%dT%H:%M:%S%z')
            }
        )

def get_old_payment_status(sender: Payment, instance: Payment, **kwargs: Any) -> None:
    if len(instance.payment_orders.all()) > 0:
        PaymentDataclass.order_id = instance.payment_orders.first().id
    PaymentDataclass.status = instance.payment_status

def get_new_payment_status(sender: Payment, instance: Payment, **kwargs: Any) -> None:
    channel_layer = get_channel_layer()

    if PaymentDataclass.status != instance.payment_status or PaymentDataclass.order_id:
        async_to_sync(channel_layer.group_send)(
            'orderStatuses',
            {
                'type': 'update_status',
                'id': PaymentDataclass.order_id,
                'payment_status': instance.payment_status
            }
        )

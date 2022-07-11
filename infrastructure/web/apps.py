from django.apps import AppConfig


class WebAppConfig(AppConfig):
    name = 'infrastructure.web'
    verbose_name = 'Клиентская часть'

    def ready(self) -> None:
        from django.db.models.signals import pre_save, post_save
        from models.order.models import Order
        from models.payment.models import Payment
        from infrastructure.web.order.signals import (
            get_old_order_status, get_old_payment_status,
            get_new_order_status, get_new_payment_status
        )

        pre_save.connect(receiver=get_old_order_status, sender=Order, dispatch_uid='get_old_order_status')
        post_save.connect(receiver=get_new_order_status, sender=Order, dispatch_uid='get_new_order_status')

        pre_save.connect(receiver=get_old_payment_status, sender=Payment, dispatch_uid='get_old_payment_status')
        post_save.connect(receiver=get_new_payment_status, sender=Payment, dispatch_uid='get_new_payment_status')

from models.payment.models import PAYMENT_STATUS_CHOICES, Payment
from models.payment_method.models import PaymentMethod
from typing import List


class PaymentService:
    @staticmethod
    def create_payment(data: dict) -> Payment:
        return Payment.objects.create(
            payment_status=data['payment_status'],
        )

    @staticmethod
    def create_unpaid_payment() -> Payment:
        return Payment.objects.create(payment_status=PAYMENT_STATUS_CHOICES[0][0])

    @staticmethod
    def get_payment_methods() -> List[PaymentMethod]:
        return PaymentMethod.objects.all()

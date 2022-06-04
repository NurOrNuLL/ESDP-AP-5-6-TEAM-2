from models.payment.models import Payment
from typing import List


class PaymentService:
    @staticmethod
    def create_payment(data: dict) -> Payment:
        return Payment.objects.create(
            payment_status=data['payment_status'],
        )

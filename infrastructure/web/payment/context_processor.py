from models.payment_method.models import PaymentMethod
from typing import Dict


def payment_methods(request) -> Dict[object, PaymentMethod]:
    return {
        'payment_methods': PaymentMethod.objects.all()
    }

from django import forms
from models.order.models import Order
from models.payment.models import Payment
from models.payment_method.models import PaymentMethod


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = []
        exclude = ['trade_point', 'contractor', 'own', 'payment']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['method', 'type']

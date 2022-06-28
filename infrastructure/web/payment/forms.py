from django import forms
from models.payment.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_status', 'details', 'method']

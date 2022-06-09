from django import forms
from models.order.models import Order
from models.payment.models import Payment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['trade_point', 'contractor', 'own', 'payment']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['method', 'type']


class OrderCreateFormStage1(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contractor', 'own']


class OrderCreateFormStage2(forms.Form):
    services = forms.CharField(required=True)
    employee = forms.MultipleChoiceField(required=True)


class OrderCreateFormStage3(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['mileage', 'note']

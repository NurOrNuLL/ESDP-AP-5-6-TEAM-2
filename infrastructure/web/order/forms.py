from django import forms
from models.order.models import Order
from models.payment.models import Payment
from models.order.validators import JSONSchemaValidator
from models.order.models import JOBS_JSON_SCHEMA


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
    jobs = forms.JSONField(required=True, validators=[JSONSchemaValidator(limit_value=JOBS_JSON_SCHEMA)])


class OrderCreateFormStage3(forms.Form):
    mileage = forms.CharField()
    note = forms.Textarea()


class OrderCreateFormStage3(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['mileage', 'note']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['version', 'jobs', 'mileage', 'note', 'price_for_pay', 'full_price']

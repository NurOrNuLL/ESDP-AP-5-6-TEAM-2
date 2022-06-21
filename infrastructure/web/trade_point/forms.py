from django import forms
from models.trade_point.models import TradePoint


class TradePointForm(forms.ModelForm):

    class Meta:
        model = TradePoint
        exclude = ['organization']

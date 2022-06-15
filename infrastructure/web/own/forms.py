from django import forms
from models.own.models import Own


class OwnForm(forms.ModelForm):

    class Meta:
        model = Own
        exclude = ['contractor']
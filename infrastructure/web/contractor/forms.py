from django import forms
from models.contractor.models import Contractor


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        exclude = ['organization']
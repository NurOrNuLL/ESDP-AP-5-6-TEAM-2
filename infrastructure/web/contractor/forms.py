from django import forms
from models.contractor.models import Contractor


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        contractor_type = forms.CharField()
        exclude = ['organization']


class ContractorUpdateForm(forms.ModelForm):
    class Meta:
        model = Contractor
        exclude = ['organization', 'IIN_or_BIN']

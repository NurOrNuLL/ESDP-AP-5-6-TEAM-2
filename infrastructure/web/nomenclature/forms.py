from django import forms
from models.nomenclature.models import Nomenclature


class NomenclatureForm(forms.ModelForm):

    class Meta:
        model = Nomenclature
        exclude = ['organization']



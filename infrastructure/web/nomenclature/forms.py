from django import forms
from models.nomenclature.models import Nomenclature


class NomenclatureForm(forms.ModelForm):

    class Meta:
        model = Nomenclature
        exclude = ['organization']


class NomenclatureImportForm(forms.Form):
    nomenclature_id = forms.IntegerField(required=True)
    excel_file = forms.FileField(required=True)


class FilterForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    category = forms.CharField(max_length=100, required=False)
    mark = forms.CharField(max_length=100, required=False)
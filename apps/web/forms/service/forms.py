from django import forms


class ServiceImportForm(forms.Form):
    excel_file = forms.FileField(required=True)

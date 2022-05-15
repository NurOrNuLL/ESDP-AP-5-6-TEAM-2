from django import forms


class FilterForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    category = forms.CharField(max_length=100, required=False)
    price_category = forms.CharField(max_length=100, required=False)

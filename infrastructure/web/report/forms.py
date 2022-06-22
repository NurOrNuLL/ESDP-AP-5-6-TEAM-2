from django import forms


class ReportDateForm(forms.Form):
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)

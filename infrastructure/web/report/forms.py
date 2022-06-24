from django import forms


class ReportDateForm(forms.Form):
    from_date = forms.DateTimeField(required=True)
    to_date = forms.DateTimeField(required=True)

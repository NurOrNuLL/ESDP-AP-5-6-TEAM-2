from django import forms
from models.employee.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name',
            'surname', 'role',
            'IIN', 'address', 'phone',
            'birthdate', 'tradepoint', 'version'
        ]

from rest_framework import serializers
from models.employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('image', )

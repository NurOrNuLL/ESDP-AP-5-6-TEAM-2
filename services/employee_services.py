import os
from typing import List

import boto3 as boto3
from models.employee.models import Employee
from django.core.exceptions import ObjectDoesNotExist

from models.trade_point.models import TradePoint
from django.http import HttpRequest
from services.trade_point_services import TradePointService


class EmployeeServices:
    @staticmethod
    def create_employee_without_image(data: dict) -> Employee:
        return Employee.objects.create(
            name=data['name'].capitalize(),
            surname=data['surname'].capitalize(),
            role=data['role'],
            IIN=data['IIN'],
            address=data['address'],
            phone=data['phone'],
            birthdate=data['birthdate'],
            tradepoint=data['tradepoint']
        )

    @staticmethod
    def create_employee_with_uuid(uuid: str, data: dict) -> Employee:
        return Employee.objects.create(
            uuid=uuid,  # noqa E126
            name=data['name'].capitalize(),
            surname=data['surname'].capitalize(),
            role=data['role'],
            IIN=data['IIN'],
            address=data['address'],
            phone=data['phone'],
            birthdate=data['birthdate'],
            tradepoint=data['tradepoint']
        )

    @staticmethod
    def get_employee() -> List['Employee']:
        return Employee.ROLE

    @staticmethod
    def get_employee_by_uuid(empUID: str) -> Employee:
        return Employee.objects.get(uuid=empUID)

    @staticmethod
    def get_employee_by_iin(empIIN: str) -> Employee:
        return Employee.objects.get(IIN=empIIN)

    @staticmethod
    def get_tradepoint() -> List['TradePoint']:
        return TradePoint.objects.all()

    @staticmethod
    def get_employees() -> List['Employee']:
        return Employee.objects.filter()

    @staticmethod
    def get_employee_by_tradepoint(tradepoint: TradePoint) -> List[Employee]:
        return Employee.objects.filter(tradepoint=tradepoint)

    @staticmethod
    def upload_image(image, empIIN):
        s3 = boto3.client('s3')
        s3.upload_fileobj(
            image, os.environ.get('AWS_BUCKET_NAME'),
            f'employee_image_{empIIN}.png'
        )

    @staticmethod
    def update_employee_without_image(emp_uid: str, cleaned_data: dict) -> Employee:
        employee = Employee.objects.get(uuid=emp_uid)
        employee.name = cleaned_data['name'].capitalize()
        employee.surname = cleaned_data['surname'].capitalize()
        employee.role = cleaned_data['role']
        employee.IIN = cleaned_data['IIN']
        employee.address = cleaned_data['address']
        employee.phone = cleaned_data['phone']
        employee.tradepoint = TradePointService.get_trade_point_from_form(cleaned_data)
        return employee

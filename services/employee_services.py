import os
from typing import List

import boto3 as boto3
from models.employee.models import Employee
from django.core.exceptions import ObjectDoesNotExist

from models.trade_point.models import TradePoint
from django.http import HttpRequest
from services.trade_point_services import TradePointServices


class EmployeeServices:
    @staticmethod
    def create_employee_without_image(data: dict) -> Employee:
        return Employee.objects.create(
            name=data['name'],
            surname=data['surname'],
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
            name=data['name'],
            surname=data['surname'],
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
    def get_tradepoint() -> List['TradePoint']:
        return TradePoint.objects.all()


    @staticmethod
    def get_attached_tradepoint_id(request: HttpRequest, uuid: str) -> int:  # noqa C901
        try:
            employee = Employee.objects.get(uuid=uuid)  # noqa F841
        except ObjectDoesNotExist:
            tradepointID = request.COOKIES.get('tradepointID')

            if tradepointID:
                return int(tradepointID)
            else:
                return TradePoint.objects.first().id
        else:
            return Employee.objects.get(uuid=uuid).tradepoint.id

    @staticmethod
    def get_employees() -> List['Employee']:
        return Employee.objects.filter()

    @staticmethod
    def get_employee_by_tradepoint(tradepoint: TradePoint) -> List[Employee]:
        return Employee.objects.filter(tradepoint=tradepoint)

    @staticmethod
    def upload_image(image, empUID):
        s3 = boto3.client('s3')
        s3.upload_fileobj(image, os.environ.get('AWS_BUCKET_NAME'), f'employee_image_{empUID}.png')

    @staticmethod
    def update_employee(emp_uid: str, data: dict) -> Employee:
        employee = Employee.objects.get(uuid=emp_uid)
        employee.image = data['image'],
        employee.name = data['name'],
        employee.surname = data['surname'],
        employee.role = data['role'],
        employee.IIN = data['IIN'],
        employee.address = data['address'],
        employee.phone = data['phone'],
        employee.tradepoint = TradePointServices.get_trade_point_from_form(data)
        return employee

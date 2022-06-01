from typing import List

from models.employee.models import Employee
from django.core.exceptions import ObjectDoesNotExist

from models.trade_point.models import TradePoint
from django.http import HttpRequest


class EmployeeServices:
    @staticmethod
    def create_employee(data: dict) -> Employee:
        return Employee.objects.create(
            name=data['name'],
            surname=data['surname'],
            role=data['role'],
            IIN=data['IIN'],
            pdf=data['pdf'],
            address=data['address'],
            phone=data['phone'],
            birthdate=data['birthdate'],
            tradepoint=data['tradepoints']
        )

    @staticmethod
    def create_employee_with_uuid(uuid: str, data: dict) -> Employee:
        return Employee.objects.create(
                uuid=uuid,
                name=data['name'],
                surname=data['surname'],
                role=data['role'],
                IIN=data['IIN'],
                pdf=data['pdf'],
                address=data['address'],
                phone=data['phone'],
                birthdate=data['birthdate'],
                tradepoint=data['tradepoint']
            )


    @staticmethod
    def get_employee() -> List['Employee']:
        return Employee.ROLE

    @staticmethod
    def get_attached_tradepoint_id(request: HttpRequest, uuid: str) -> int:
        try:
            employee = Employee.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            tradepointID = request.COOKIES.get('tradepointID')

            if tradepointID:
                return int(tradepointID)
            else:
                return TradePoint.objects.first().id
        else:
            return Employee.objects.get(uuid=uuid).tradepoint.id

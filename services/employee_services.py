from typing import List

from models.employee.models import Employee


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
            tradepoints=data['tradepoints']
        )

    @staticmethod
    def get_employee() -> List['Employee']:
        return Employee.ROLE

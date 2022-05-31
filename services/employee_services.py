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

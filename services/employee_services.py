import io
from typing import List

import boto3
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
            image=data['image'],
            address=data['address'],
            phone=data['phone'],
            birthdate=data['birthdate'],
            tradepoint=data['tradepoint']
        )

    @staticmethod
    def create_employee_with_uuid(uuid: str, data: dict) -> Employee:
        return Employee.objects.create(
                uuid=uuid,
                name=data['name'],
                surname=data['surname'],
                role=data['role'],
                IIN=data['IIN'],
                image=data['image'],
                address=data['address'],
                phone=data['phone'],
                birthdate=data['birthdate'],
                tradepoint=data['tradepoint']
            )


    @staticmethod
    def get_employee() -> List['Employee']:
        return Employee.ROLE

    @staticmethod
    def get_tradepoint() -> List['TradePoint']:
        return TradePoint.objects.all()

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

    @staticmethod
    def upload_image(local_path, path, bucket_name='test.aspa', acl='public-read'):
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.us-east-2.amazonaws.com/',
            aws_access_key_id='AKIA2M2OPPDRB7G7CJ7A',
            aws_secret_access_key='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',
            region_name='us-east-2',
        )
        with open(local_path, 'rb') as f:
            file = io.BytesIO(f.read())
            s3_client.upload_fileobj(
                file,
                bucket_name,
                path,
                ExtraArgs={
                    'ACL': acl
                }
            )

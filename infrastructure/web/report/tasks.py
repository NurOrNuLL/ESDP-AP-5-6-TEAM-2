import os

from celery import shared_task
from decimal import Decimal
from services.order_services import OrderService
from services.employee_services import EmployeeServices
from datetime import datetime
from typing import Dict, Any, List
import time
import json
import boto3
from botocore.exceptions import ClientError
from models.report.models import Report


@shared_task
def get_reports_from_aws(tradepoint_id: int) -> List[Dict[str, Any]]:
    reports = Report.objects.filter(tradepoint_id=tradepoint_id)
    reports_from_aws = []

    for report in reports:
        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        result = client.get_object(Bucket=os.environ.get('AWS_BUCKET_NAME'), Key=f'report {report.report_uuid}')
        reports_from_aws.append(json.loads(result["Body"].read().decode()))

    return reports_from_aws


@shared_task
def upload_report_to_bucket(report: dict) -> str:
    try:
        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(report),
            Bucket=os.environ.get('AWS_BUCKET_NAME'),
            Key=f'report {report["uuid"]}'
        )
    except ClientError:
        return False
    else:
        Report.objects.create(report_uuid=report['uuid'], tradepoint_id=report['tradepoint_id'])

    return True


@shared_task
def get_report(from_date: datetime.date, to_date: datetime.date, report_type: int, tp_id: int) -> Dict[str, Any]:
    from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
    to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

    orders = OrderService.get_finished_orders_in_period(from_date, to_date, tp_id)

    time.sleep(1)

    if report_type == 1:
        result = {
            'report_type': report_type,
            'paidOrders': [],
            'unpaidOrders': [],
            'employeeSalary': [],
            'total': Decimal('0.00'),
            'totalPaid': Decimal('0.00'),
            'totalUnpaid': Decimal('0.00'),
            'garanty': Decimal('0.00')
        }

        employeeIINs = []

        for order in orders:
            if order.payment.payment_status == '????????????????':
                result['paidOrders'].append({
                    'created_at': datetime.strftime(order.created_at, '%d.%m.%Y'),
                    'finished_at': datetime.strftime(order.finished_at, '%d.%m.%Y'),
                    'order_id': order.id,
                    'contractor_id': order.contractor.id,
                    'contractor': order.contractor.name,
                    'own': order.own.number if order.own.is_part is False else order.own.name,
                    'garanty': order.full_price - order.price_for_pay,
                    'total': order.price_for_pay,
                })
            else:
                result['unpaidOrders'].append({
                    'created_at': datetime.strftime(order.created_at, '%d.%m.%Y'),
                    'finished_at': datetime.strftime(order.finished_at, '%d.%m.%Y'),
                    'order_id': order.id,
                    'contractor_id': order.contractor.id,
                    'contractor': order.contractor.name,
                    'own': order.own.number if order.own.is_part is False else order.own.name,
                    'garanty': order.full_price - order.price_for_pay,
                    'total': order.price_for_pay,
                })

            for job in order.jobs:
                result['total'] += job['???????? ????????????']

                if order.payment.payment_status == '????????????????':
                    if not job['????????????????']:
                        result['totalPaid'] += job['???????? ????????????']
                    else:
                        result['garanty'] += job['???????? ????????????']
                else:
                    if not job['????????????????']:
                        result['totalUnpaid'] += job['???????? ????????????']
                    else:
                        result['garanty'] += job['???????? ????????????']

                totalIncomeEmployee = (Decimal(f'{job["???????? ????????????"]}.00') / 2) / len(job['??????????????'])

                for employee in job['??????????????']:
                    if employee['??????'] in employeeIINs:
                        index = result['employeeSalary'].index([e for e in result['employeeSalary'] if e['??????'] == employee['??????']][0])
                        result['employeeSalary'][index]['????????????????'] += totalIncomeEmployee.quantize(Decimal('1.00'))
                    else:
                        result['employeeSalary'].append(
                            {
                                '????????????????????????': f"{EmployeeServices.get_employee_by_iin(employee['??????']).name} {EmployeeServices.get_employee_by_iin(employee['??????']).surname}",
                                '??????': EmployeeServices.get_employee_by_iin(employee['??????']).IIN,
                                '????????????????': totalIncomeEmployee.quantize(Decimal('1.00'))
                            }
                        )
                        employeeIINs.append(employee['??????'])

        return result
    elif report_type == 2:
        result = {
            'report_type': report_type,
            'paidOrders': [],
            'unpaidOrders': [],
            'total': Decimal('0.00'),
            'totalPaid': Decimal('0.00'),
            'totalUnpaid': Decimal('0.00'),
            'garanty': Decimal('0.00')
        }

        for order in orders:
            if order.payment.payment_status == '????????????????':
                result['paidOrders'].append({
                    'created_at': datetime.strftime(order.created_at, '%d.%m.%Y'),
                    'finished_at': datetime.strftime(order.finished_at, '%d.%m.%Y'),
                    'order_id': order.id,
                    'contractor_id': order.contractor.id,
                    'contractor': order.contractor.name,
                    'own': order.own.number if order.own.is_part is False else order.own.name,
                    'garanty': order.full_price - order.price_for_pay,
                    'total': order.price_for_pay,
                })
            else:
                result['unpaidOrders'].append({
                    'created_at': datetime.strftime(order.created_at, '%d.%m.%Y'),
                    'finished_at': datetime.strftime(order.finished_at, '%d.%m.%Y'),
                    'order_id': order.id,
                    'contractor_id': order.contractor.id,
                    'contractor': order.contractor.name,
                    'own': order.own.number if order.own.is_part is False else order.own.name,
                    'garanty': order.full_price - order.price_for_pay,
                    'total': order.price_for_pay,
                })

            for job in order.jobs:
                result['total'] += job['???????? ????????????']

                if order.payment.payment_status == '????????????????':
                    if not job['????????????????']:
                        result['totalPaid'] += job['???????? ????????????']
                    else:
                        result['garanty'] += job['???????? ????????????']
                else:
                    if not job['????????????????']:
                        result['totalUnpaid'] += job['???????? ????????????']
                    else:
                        result['garanty'] += job['???????? ????????????']

        return result
    elif report_type == 3:
        result = {
            'report_type': report_type,
            'employeeSalary': []
        }

        employeeIINs = []

        for order in orders:
            for job in order.jobs:
                totalIncomeEmployee = (Decimal(f'{job["???????? ????????????"]}.00') / 2) / len(job['??????????????'])

                for employee in job['??????????????']:
                    if employee['??????'] in employeeIINs:
                        index = result['employeeSalary'].index([e for e in result['employeeSalary'] if e['??????'] == employee['??????']][0])
                        result['employeeSalary'][index]['????????????????'] += totalIncomeEmployee.quantize(Decimal('1.00'))
                    else:
                        result['employeeSalary'].append(
                            {
                                '????????????????????????': f"{EmployeeServices.get_employee_by_iin(employee['??????']).name} {EmployeeServices.get_employee_by_iin(employee['??????']).surname}",
                                '??????': EmployeeServices.get_employee_by_iin(employee['??????']).IIN,
                                '??????????????': EmployeeServices.get_employee_by_iin(employee['??????']).phone,
                                '????????????????': totalIncomeEmployee.quantize(Decimal('1.00'))
                            }
                        )
                        employeeIINs.append(employee['??????'])

        return result

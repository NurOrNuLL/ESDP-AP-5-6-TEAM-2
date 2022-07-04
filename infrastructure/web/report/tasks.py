import json
from celery import shared_task
from decimal import Decimal
from services.order_services import OrderService
from services.employee_services import EmployeeServices
from datetime import datetime
from typing import Dict, Any
from time import sleep


@shared_task
def get_report(from_date: datetime.date, to_date: datetime.date, tpID: int) -> Dict[str, Any]:
    from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
    to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

    result = {
        'paidOrders': [],
        'unpaidOrders': [],
        'employeeSalary': [],
        'total': Decimal('0.00'),
        'totalPaid': Decimal('0.00'),
        'totalUnpaid': Decimal('0.00'),
        'garanty': Decimal('0.00')
    }

    orders = OrderService.get_finished_orders_in_period(from_date, to_date, tpID)
    employeeIINs = []

    for order in orders:
        if order.payment.payment_status == 'Оплачено':
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
            result['total'] += job['Цена услуги']

            if order.payment.payment_status == 'Оплачено':
                if not job['Гарантия']:
                    result['totalPaid'] += job['Цена услуги']
                else:
                    result['garanty'] += job['Цена услуги']
            else:
                if not job['Гарантия']:
                    result['totalUnpaid'] += job['Цена услуги']
                else:
                    result['garanty'] += job['Цена услуги']

            totalIncomeEmployee = (Decimal(f'{job["Цена услуги"]}.00') / 2) / len(job['Мастера'])

            for employee in job['Мастера']:
                if employee['ИИН'] in employeeIINs:
                    index = result['employeeSalary'].index([e for e in result['employeeSalary'] if e['ИИН'] == employee['ИИН']][0])
                    result['employeeSalary'][index]['Зарплата'] += totalIncomeEmployee.quantize(Decimal('1.00'))
                else:
                    result['employeeSalary'].append(
                        {
                            'Наименование': f"{EmployeeServices.get_employee_by_iin(employee['ИИН']).name} {EmployeeServices.get_employee_by_iin(employee['ИИН']).surname}",
                            'ИИН': EmployeeServices.get_employee_by_iin(employee['ИИН']).IIN,
                            'Зарплата': totalIncomeEmployee.quantize(Decimal('1.00'))
                        }
                    )
                    employeeIINs.append(employee['ИИН'])

    sleep(2)

    return result

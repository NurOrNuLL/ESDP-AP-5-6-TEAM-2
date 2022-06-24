from celery import shared_task
from decimal import Decimal
from services.order_services import OrderService
from services.employee_services import EmployeeServices
from datetime import datetime
from typing import Dict, Any


@shared_task
def get_report(from_date: datetime.date, to_date: datetime.date, tpID: int) -> Dict[str, Any]:
        result = {
            'paidJobs': [],
            'unpaidJobs': [],
            'employeeSalary': [],
            'total': Decimal('0.00'),
            'totalPaid': Decimal('0.00'),
            'totalUnpaid': Decimal('0.00'),
            'garanty': Decimal('0.00')
        }

        orders = OrderService.get_finished_orders_in_period(from_date, to_date, tpID)
        employeeIINs = []

        for order in orders:
            for job in order.jobs:
                result['total'] += job['Цена услуги']

                if order.payment.payment_status == 'Оплачено':
                    result['paidJobs'].append(job)

                    if not job['Гарантия']:
                        result['totalPaid'] += job['Цена услуги']
                    else:
                        result['garanty'] += job['Цена услуги']
                else:
                    result['unpaidJobs'].append(job)

                    if not job['Гарантия']:
                        result['totalUnpaid'] += job['Цена услуги']
                    else:
                        result['garanty'] += job['Цена услуги']

                totalIncomeEmployee = (Decimal(f'{job["Цена услуги"]}.00') / 2) / len(job['Мастера'])

                for employee in job['Мастера']:
                    if employee['ИИН'] in employeeIINs:
                        result['employeeSalary'][result['employeeSalary'].index(
                            [e for e in result['employeeSalary'] if e['ИИН'] == employee['ИИН']][0])]['Зарплата'] += totalIncomeEmployee
                    else:
                        result['employeeSalary'].append(
                            {
                                'Наименование': f"{EmployeeServices.get_employee_by_iin(employee['ИИН']).name} {EmployeeServices.get_employee_by_iin(employee['ИИН']).surname}",
                                'ИИН': int(EmployeeServices.get_employee_by_iin(employee['ИИН']).IIN),
                                'Зарплата': totalIncomeEmployee.quantize(Decimal('1.00'))
                            }
                        )

            if len(result['employeeSalary']) > 0:
                for employeeSalary in result['employeeSalary']:
                    employeeIINs.append(employeeSalary['ИИН'])

        return result

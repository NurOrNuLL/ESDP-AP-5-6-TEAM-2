import os

import tablib
from django.http import HttpResponse, HttpResponseRedirect
from models.nomenclature.models import Nomenclature
from models.organization.models import Organization
from io import BytesIO
import pandas
from typing import List
import jsonschema
import json
from urllib.parse import quote
import datetime
import boto3

File = str
JSON = dict
JSONSchema = dict


class ReportService:
    @staticmethod
    def download_a_exel_file_to_user(file_data: dict, file_extension: str):
        if not file_data['report_type'] == 3:
            paid_data_structure = ReportService.prepare_order_data_for_excel(file_data['paidOrders'])
            paid_data = pandas.DataFrame(paid_data_structure)
            unpaid_data_structure = ReportService.prepare_order_data_for_excel(file_data['unpaidOrders'])
            unpaid_data = pandas.DataFrame(unpaid_data_structure)
            total_data_structure = ReportService.prepare_total_data_for_excel(file_data)
            total_data = pandas.DataFrame(total_data_structure)
            indexing = [paid_data, unpaid_data, total_data]
            if file_data['report_type'] == 1:
                salary_data_structure = ReportService.prepare_salary_data_for_excel(file_data['employeeSalary'])
                salary_data = pandas.DataFrame(salary_data_structure)
                indexing.append(salary_data)
            for i in indexing:
                i.index += 1
            with BytesIO() as b:
                writer = pandas.ExcelWriter(b, engine='xlsxwriter')
                paid_data.to_excel(writer, sheet_name='Оплаченные работы')
                unpaid_data.to_excel(writer, sheet_name='Неоплаченные работы')
                if file_data['report_type'] == 1:
                    salary_data.to_excel(writer, sheet_name='Зарплаты мастерам')
                total_data.to_excel(writer, sheet_name='Итог')
                writer.save()
                return ReportService.response_sender(b, file_extension)
        else:
            salary_data_structure = ReportService.prepare_salary_data_for_excel(file_data['employeeSalary'])
            salary_data = pandas.DataFrame(salary_data_structure)
            salary_data.index += 1
            with BytesIO() as b:
                writer = pandas.ExcelWriter(b, engine='xlsxwriter')
                salary_data.to_excel(writer, sheet_name='Запрлаты мастерам')
                writer.save()
                return ReportService.response_sender(b, file_extension)

    @staticmethod
    def response_sender(data: bytes, file_extension: str) -> HttpResponse or HttpResponseRedirect:
        file_name = "report" + '_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"))
        try:
            file_name.encode('ascii')
            file_expr = 'filename="{}.{}"'.format(file_name, file_extension)
        except UnicodeEncodeError:
            file_expr = "filename*=utf-8''{}.{}".format(quote(file_name), file_extension)
        content_type = 'application/vnd.ms-excel'
        response = HttpResponse(data.getvalue(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; {}'.format(file_expr)
        return response

    @staticmethod
    def prepare_total_data_for_excel(file_data):
        data = {'Критерий': [], 'Сумма': []}
        data['Критерий'].extend(['Общая реализация', 'Гарантия', 'Оплаченные работы', 'Неоплаченные работы'])
        data['Сумма'].extend([file_data['total'], file_data['garanty'], file_data['totalPaid'], file_data['totalUnpaid']])
        return data

    @staticmethod
    def prepare_salary_data_for_excel(file_data):
        data = {'Мастер': [], 'ИИН': [], 'Зарплата': []}
        for i in file_data:
            data['Мастер'].append(i['Наименование'])
            data['ИИН'].append(i['ИИН'])
            data['Зарплата'].append(i['Зарплата'])
        return data

    @staticmethod
    def prepare_order_data_for_excel(file_data):
        data = {'Дата создания': [], 'Дата завершения': [], 'Контрагент': [], 'Номер авто/Запчасть': [], 'Гарантия': [], 'Сумма': []}
        for i in file_data:
            data['Дата создания'].append(i['created_at'])
            data['Дата завершения'].append(i['finished_at'])
            data['Контрагент'].append(i['contractor'])
            data['Номер авто/Запчасть'].append(i['own'])
            data['Гарантия'].append(i['garanty'])
            data['Сумма'].append(i['total'])
        return data

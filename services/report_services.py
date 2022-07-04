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

File = str
JSON = dict
JSONSchema = dict


class ReportService:
    @staticmethod
    def download_a_exel_file_to_user(file_data, file_extension):
        paid_data_structure = ReportService.prepare_jobs_data_for_excel(file_data['paidJobs'])
        paid_data = pandas.DataFrame(paid_data_structure)
        unpaid_data_structure = ReportService.prepare_jobs_data_for_excel(file_data['unpaidJobs'])
        unpaid_data = pandas.DataFrame(unpaid_data_structure)
        salary_data_structure = ReportService.prepare_salary_data_for_excel(file_data['employeeSalary'])
        salary_data = pandas.DataFrame(salary_data_structure)
        total_data_structure = ReportService.prepare_total_data_for_excel(file_data)
        total_data = pandas.DataFrame(total_data_structure)
        indexing = [paid_data, unpaid_data, salary_data, total_data]
        for i in indexing:
            i.index = i.index +1
        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            paid_data.to_excel(writer, sheet_name='Оплаченные работы')
            unpaid_data.to_excel(writer, sheet_name='Неоплаченные работы')
            salary_data.to_excel(writer, sheet_name='Запрлаты мастерам')
            total_data.to_excel(writer, sheet_name='Итог')
            writer.save()
            file_name = "report" + '_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"))
            try:
                file_name.encode('ascii')
                file_expr = 'filename="{}.{}"'.format(file_name, file_extension)
            except UnicodeEncodeError:
                file_expr = "filename*=utf-8''{}.{}".format(quote(file_name), file_extension)
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + file_name + f'.{file_extension}"'
            return response

    @staticmethod
    def prepare_total_data_for_excel(file_data):
        data = {'Критерий': [], 'Сумма': []}
        data['Критерий'].extend(['Общая реализация', 'Гарантия', 'Оплаченные работы', 'Неоплаченные работы'])
        data['Сумма'].extend([file_data['total'], file_data['garanty'], file_data['totalPaid'], file_data['totalUnpaid']])
        return data

    @staticmethod
    def prepare_salary_data_for_excel(file_data):
        data = {'Наименование': [], 'ИИН': [], 'Зарплата': []}
        for i in file_data:
            data['Наименование'].append(i['Наименование'])
            data['ИИН'].append(i['ИИН'])
            data['Зарплата'].append(i['Зарплата'])
        return data

    @staticmethod
    def prepare_jobs_data_for_excel(file_data):
        data = {'Название услуги': [], 'Категория': [], 'Марка': [], 'Мастера': [], 'Гарантия': [], 'Цена': []}
        for i in file_data:
            data['Название услуги'].append(i['Название услуги'])
            data['Категория'].append(i['Категория услуги'])
            data['Марка'].append(i['Марка услуги'])
            data['Мастера'].append(i['Мастера'])
            data['Гарантия'].append(i['Гарантия'])
            data['Цена'].append(i['Цена услуги'])
        return data

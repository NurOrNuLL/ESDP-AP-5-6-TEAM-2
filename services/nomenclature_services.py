import tablib
from django.http import HttpResponse, HttpResponseRedirect
from models.nomenclature.models import Nomenclature
from models.organization.models import Organization
import pandas
from typing import List
import jsonschema
import json
from urllib.parse import quote

File = str
JSON = dict
JSONSchema = dict


class NomenclatureService:
    @staticmethod
    def create_nomenclature(data: dict) -> Nomenclature:
        return Nomenclature.objects.create(
            name=data['name'],
            organization=Organization.objects.get(id=1),
        )

    @staticmethod
    def get_all_nomenclatures() -> List['Nomenclature']:
        return Nomenclature.objects.all()

    @staticmethod
    def get_nomenclature_by_id(nomenclature_id: int) -> Nomenclature:
        return Nomenclature.objects.get(id=nomenclature_id)

    @staticmethod
    def parse_excel_to_json(file: File) -> JSON:
        new_file = str(file)
        if new_file.endswith('xlsx'):
            data = pandas.read_excel(file)
        elif new_file.endswith('xls'):
            data = pandas.read_excel(file)
        return data.to_json(orient='records').replace('null', '""')

    @staticmethod
    def validate_json(data: JSON, json_schema: JSONSchema) -> True or False:
        try:
            jsonschema.validate(json.loads(data), json_schema)
            return data
        except jsonschema.exceptions.ValidationError:
            return False

    @staticmethod
    def import_services(data: JSON, nomenclature_id: int) -> None:
        nomenclature = NomenclatureService.get_nomenclature_by_id(
            nomenclature_id=nomenclature_id
        )
        nomenclature.services = json.loads(data)
        nomenclature.save()

    @staticmethod
    def get_filtered_services(
            nomenclature_id: int,
            search: str = '',
            category: str = '',
            mark: str = '') -> List['Nomenclature']:
        services = NomenclatureService.get_nomenclature_by_id(
            nomenclature_id=nomenclature_id
        ).services
        filtered_services = []

        for service in services:
            if (
                    (
                            search.lower() in service['Название'].lower()  # noqa E126
                            or search.lower() in service['Категория'].lower()
                            or search.lower() in service['Марка'].lower()
                    )
                    and category in service['Категория']
                    and mark in service['Марка']
            ):
                filtered_services.append(service)

        return filtered_services

    @staticmethod
    def response_sender(
            data: str,
            file_extension: str,
            name: str) -> HttpResponse or HttpResponseRedirect:
        response = HttpResponse(data)
        file_name = "price_" + name
        try:
            file_name.encode('ascii')
            file_expr = 'filename="{}.{}"'.format(file_name, file_extension)
        except UnicodeEncodeError:
            file_expr = "filename*=utf-8''{}.{}".format(quote(file_name), file_extension)
        response['Content-Disposition'] = 'attachment; {}'.format(file_expr)
        return response

    @staticmethod
    def download_a_exel_file_to_user(file_data, file_extension):
        headers = ['Цена', 'Марка', 'Название', 'Категория', 'Примечание']
        data = tablib.Dataset(headers=headers)
        for i in file_data:
            data.append(i.values())
            file_data = data.export(file_extension)
        return file_data

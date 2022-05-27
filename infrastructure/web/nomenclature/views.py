import tablib
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import NomenclatureForm, NomenclatureImportForm
from django.shortcuts import render, redirect
from services.nomenclature_services import create_nomenclature
import json
from models.nomenclature.models import Nomenclature, SERVICE_JSON_FIELD_SCHEMA
import pandas
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .serializers import NomenclatureFilterSerializer
from models.nomenclature.category_choices import CATEGORY_CHOICES, MARK_CHOICES
import jsonschema


class NomenclatureImportView(TemplateView):
    template_name = 'nomenclature/list.html'
    form_class = NomenclatureImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomenclatures'] = Nomenclature.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = pandas.read_excel(form.cleaned_data['excel_file'])
            json_data = data.to_json(orient='records').replace('null', '""')

            try:
                jsonschema.validate(json.loads(json_data), SERVICE_JSON_FIELD_SCHEMA)
            except jsonschema.exceptions.ValidationError:
                context = self.get_context_data(
                    error='Неверный excel, проверте наличие полей: "Название", "Категория", "Примечание", "Марка", "Цена"')

                return render(self.request, template_name=self.template_name, context=context)
            else:
                nomenclature = Nomenclature.objects.get(id=form.cleaned_data['nomenclature_id'])
                nomenclature.services = json.loads(json_data)
                nomenclature.save()

                return redirect('nomenclature_list', orgID=self.kwargs['orgID'])


class NomenclaturesServiceListView(TemplateView):
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['marks'] = MARK_CHOICES
        context['nomenclatures'] = Nomenclature.objects.all()
        return context


class NomenclatureItemsFilterApiView(GenericAPIView):
    serializer_class = NomenclatureFilterSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)

        if serializer.is_valid():
            filtered_data = self.get_filtered_services(
                serializer.data.get('search'),
                serializer.data.get('category'),
                serializer.data.get('mark')
            )

            paginated_data = self.get_paginated_data_page_number(
                filtered_data,
                page=serializer.data.get('page'),
                limit=serializer.data.get('limit')
            )

            return Response(paginated_data)
        else:
            return Response(serializer.errors)

    def get_filtered_services(self, search='', category='', mark=''):
        services = Nomenclature.objects.get(id=self.kwargs['id']).services
        filtered_services = []

        for service in services:
            if (
                    (
                            search.lower() in service['Название'].lower()
                            or search.lower() in service['Категория'].lower()
                            or search.lower() in service['Марка'].lower()
                    )
                    and category in service['Категория']
                    and mark in service['Марка']
            ):
                filtered_services.append(service)

        return filtered_services

    def get_paginated_data_page_number(self, data, page=1, limit=None):
        paginator = Paginator(data, limit)
        page_number = paginator.num_pages
        paginated_data = paginator.page(page).object_list

        return {
            "services": paginated_data,
            "page_number": page_number
        }


class NomenclatureCreate(TemplateView):
    template_name = 'nomenclature/nomenclature_create.html'
    form_class = NomenclatureForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            create_nomenclature(form.cleaned_data)
            return redirect('home', orgID=1)

        return render(request, self.template_name, {'form': form})


class NomenclatureExportView(TemplateView):
    template_name = 'nomenclature/list.html'
    main_data = ''

    def get(self, request, *args, **kwargs):
        nomenclature_id = request.GET.get('nomenclature_id')
        extension = request.GET.get('extension')
        nomenclatures = Nomenclature.objects.all()
        headers = []
        for nomenclature in list(nomenclatures):
            if int(nomenclature_id) == nomenclature.id:
                if nomenclature.services:
                    headers = [list(i.keys()) for i in nomenclature.services]
                    data = tablib.Dataset(headers=headers[0])
                    for i in nomenclature.services:
                        data.append(i.values())
                        self.main_data = data.export(extension)
                    response = HttpResponse(self.main_data)
                    response['Content-Disposition'] = f'attachment; filename="price.{extension}"'
                    return response
                else:
                    data = tablib.Dataset()
                    self.main_data = data.export(extension)
                    response = HttpResponse(self.main_data)
                    response['Content-Disposition'] = f'attachment; filename="price.{extension}"'
                    return response

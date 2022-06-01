import tablib
from django.views.generic import TemplateView

from services.employee_services import EmployeeServices
from .forms import NomenclatureForm, NomenclatureImportForm
from django.shortcuts import render, redirect
from services.nomenclature_services import NomenclatureService
from models.nomenclature.models import Nomenclature, SERVICE_JSON_FIELD_SCHEMA
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .serializers import NomenclatureFilterSerializer
from models.nomenclature.category_choices import CATEGORY_CHOICES, MARK_CHOICES
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from typing import List, Dict, Any


class NomenclatureImportView(TemplateView):
    template_name = 'nomenclature/list.html'
    form_class = NomenclatureImportForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['excel_file']
            data = NomenclatureService.parse_excel_to_json(file)

            if not NomenclatureService.validate_json(data, SERVICE_JSON_FIELD_SCHEMA):
                context = self.get_context_data(error='Некорректный excel, проверте его содержимое и расширение')

                return render(self.request, template_name=self.template_name, context=context)
            else:
                NomenclatureService.import_services(data, form.cleaned_data['nomenclature_id'])

                return redirect('nomenclature_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])


class NomenclaturesServiceListView(TemplateView):
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['marks'] = MARK_CHOICES
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        return context


class NomenclatureItemsFilterApiView(GenericAPIView):
    serializer_class = NomenclatureFilterSerializer
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> JsonResponse:
        serializer = self.serializer_class(data=request.GET)

        if serializer.is_valid():
            filtered_data = NomenclatureService.get_filtered_services(
                nomenclature_id=self.kwargs['id'],
                search=serializer.data.get('search'),
                category=serializer.data.get('category'),
                mark=serializer.data.get('mark')
            )

            paginated_data = self.get_paginated_data_page_number(
                filtered_data,
                page=serializer.data.get('page'),
                limit=serializer.data.get('limit')
            )

            return Response(paginated_data)
        else:
            return Response(serializer.errors)

    def get_paginated_data_page_number(self, data: List['Nomenclature'], page: int = 1, limit: int = None) -> dict:

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

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST)

        if form.is_valid():
            NomenclatureService.create_nomenclature(form.cleaned_data)
            return redirect('home_redirect')

        return render(request, self.template_name, {'form': form})


class NomenclatureExportView(TemplateView):
    """Экспорт прайса по выбранной номенклатуре"""
    template_name = 'nomenclature/list.html'
    main_data = ''

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        nomenclature_id = request.GET.get('nomenclature_id')
        extension = request.GET.get('extension')
        nomenclatures = NomenclatureService.get_all_nomenclatures()
        for nomenclature in list(nomenclatures):
            if int(nomenclature_id) == nomenclature.id:
                if nomenclature.services:
                    self.main_data = NomenclatureService.download_a_exel_file_to_user(
                        extension=extension, services=nomenclature.services
                    )
                    return NomenclatureService.response_sender(
                        data=self.main_data, file_extension=extension
                    )
                else:
                    self.main_data = NomenclatureService.download_a_exel_file_to_user(
                        extension=extension, services=nomenclature.services
                    )
                    return NomenclatureService.response_sender(
                        data=self.main_data, file_extension=extension
                    )
        context = self.get_context_data(error='Добавьте номенклатуру')
        return render(self.request, template_name=self.template_name, context=context)


class NomenclatureFormForImpost(GenericAPIView):
    """Эскпорт формы exel для заполнения нового прайса"""
    template_name = 'nomenclature/list.html'
    exel_form = ''

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        extension = request.GET.get('extension')
        headers = ['Цена', 'Марка', 'Название', 'Категория', 'Примечание']
        data = tablib.Dataset(headers=headers)
        self.exel_form = data.export(extension)
        return NomenclatureService.response_sender(
            data=self.exel_form, file_extension=extension
        )

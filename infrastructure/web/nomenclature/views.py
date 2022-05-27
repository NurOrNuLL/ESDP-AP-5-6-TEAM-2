import tablib
from django.http import HttpResponse
from django.views.generic import TemplateView
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
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from typing import List


class NomenclatureImportView(TemplateView):
    template_name = 'nomenclature/list.html'
    form_class = NomenclatureImportForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()

        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = NomenclatureService.parse_excel_to_json(form.cleaned_data['excel_file'])


            if not NomenclatureService.validate_json(data, SERVICE_JSON_FIELD_SCHEMA):
                context = self.get_context_data(error='Некорректный excel')


                return render(self.request, template_name=self.template_name, context=context)
            else:
                NomenclatureService.import_services(data, form.cleaned_data['nomenclature_id'])

                return redirect('nomenclature_list', orgID=self.kwargs['orgID'])


class NomenclaturesServiceListView(TemplateView):
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['marks'] = MARK_CHOICES
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()
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

    def get_paginated_data_page_number(self, data: List['Nomenclature'], page: int=1, limit: int=None) -> dict:

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

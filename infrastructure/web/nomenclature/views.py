import tablib
from django.views.generic import TemplateView
from services.employee_services import EmployeeServices
from .forms import NomenclatureForm, NomenclatureImportForm
from django.shortcuts import render, redirect, reverse
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
import json
from celery.result import AsyncResult
from celery_progress.backend import Progress
from ..nomenclature.tasks.import_exel import import_exel_file
from ..nomenclature.tasks.export_exel import export_exel_file
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin


class NomenclatureImportView(ResetOrderCreateFormDataMixin, TemplateView):
    """Импорт прайса для выбранной номенклатуры"""
    template_name = 'nomenclature/list.html'
    form_class = NomenclatureImportForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

    def post(
            self, request: HttpRequest,
            *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['excel_file']
            nomenclature_id = form.cleaned_data['nomenclature_id']
            data = NomenclatureService.parse_excel_to_json(file)
            validated_data = NomenclatureService.validate_json(
                data, SERVICE_JSON_FIELD_SCHEMA
            )
            if validated_data:
                task = import_exel_file.delay(file=validated_data, nom_id=nomenclature_id)
                return HttpResponse(json.dumps(
                    {"task_id": task.id}), content_type='application/json'
                )
            else:
                context = self.get_context_data(
                    error='Некорректный excel, проверте его содержимое и расширение'
                )
                return render(
                    self.request, template_name=self.template_name, context=context
                )


class NomenclaturesServiceListView(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['marks'] = MARK_CHOICES
        context['nomenclatures'] = NomenclatureService.get_all_nomenclatures()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        context = self.get_context_data()
        if request.session.get('error'):
            context['error'] = request.session['error']
            del request.session['error']
        return render(request, self.template_name, context)


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

    def get_paginated_data_page_number(
            self, data: List['Nomenclature'], page: int = 1, limit: int = None
    ) -> dict:

        paginator = Paginator(data, limit)
        page_number = paginator.num_pages
        paginated_data = paginator.page(page).object_list

        return {
            "services": paginated_data,
            "page_number": page_number
        }


class NomenclatureCreate(ResetOrderCreateFormDataMixin, TemplateView):
    template_name = 'nomenclature/nomenclature_create.html'
    form_class = NomenclatureForm

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

    def post(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST)

        if form.is_valid():
            NomenclatureService.create_nomenclature(form.cleaned_data)
            return redirect('home_redirect')

        context = self.get_context_data()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        context['form'] = form

        return render(request, self.template_name, context)


class NomenclatureExportView(ResetOrderCreateFormDataMixin, TemplateView):
    """Экспорт прайса по выбранной номенклатуре"""
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        return context

    def get(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        self.delete_order_data_from_session(request)

        nomenclature_id = request.GET.get('nomenclature_id')
        extension = request.GET.get('extension')
        task = export_exel_file.delay(nomenclature_pk=nomenclature_id, extension=extension)
        return HttpResponse(json.dumps(
            {"task_id": task.id}), content_type='application/json'
        )


class NomenclatureDownloadView(ResetOrderCreateFormDataMixin, TemplateView):
    """При удачном выполнении задачи выдает загруженный файл"""
    template_name = 'nomenclature/list.html'
    services_file = ''

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        return context

    def get(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        self.delete_order_data_from_session(request)

        celery_result = AsyncResult(request.GET.get('task_id'))
        main_data = celery_result.result.get('main_data')
        extension = celery_result.result.get('extension')
        nomenclature_pk = celery_result.result.get('nomenclature_pk')
        if nomenclature_pk is not None:
            picked_nomenclature = Nomenclature.objects.get(pk=int(nomenclature_pk))
        else:
            picked_nomenclature = ''

        if main_data is False:
            request.session['error'] = 'Отсутсвуют прайсы или номенклатура'
            url = reverse('nomenclature_list', kwargs={'orgID': 1,
                                                       'tpID': EmployeeServices.get_attached_tradepoint_id(  # noqa E501
                                                           self.request, self.request.user.uuid)}  # noqa E501
                          )
            return HttpResponseRedirect(url)
        else:
            self.services_file = NomenclatureService.download_a_exel_file_to_user(
                file_data=main_data,
                file_extension=extension
            )
            return NomenclatureService.response_sender(
                data=self.services_file, file_extension=extension,
                name=str(picked_nomenclature)
            )


class NomenclatureFormForImpost(GenericAPIView):
    """Эскпорт формы exel для заполнения нового прайса"""
    template_name = 'nomenclature/list.html'
    exel_form = ''

    def get(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        extension = request.GET.get('extension')
        headers = ['Цена', 'Марка', 'Название', 'Категория', 'Примечание']
        data = tablib.Dataset(headers=headers)
        self.exel_form = data.export(extension)
        return NomenclatureService.response_sender(
            data=self.exel_form, file_extension=extension
        )


class NomenclatureProgressView(ResetOrderCreateFormDataMixin, TemplateView):
    """Для получения данных о 100% загрузке"""
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        task_id = AsyncResult(request.GET.get('task_id'))
        if task_id:
            progress = Progress(task_id)
            return HttpResponse(
                json.dumps(progress.get_info()),
                content_type='application/json'
            )
        raise Http404

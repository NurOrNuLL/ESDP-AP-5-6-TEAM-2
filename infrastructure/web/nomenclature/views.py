import tablib
from concurrency.api import disable_concurrency
from django.views.generic import TemplateView
from services.employee_services import EmployeeServices
from services.trade_point_services import TradePointServices
from .forms import NomenclatureForm, NomenclatureImportForm
from django.shortcuts import render, redirect, reverse
from services.nomenclature_services import NomenclatureService
from models.nomenclature.models import Nomenclature, SERVICE_JSON_FIELD_SCHEMA
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .serializers import NomenclatureFilterSerializer, NomenclatureUpdateSerializer
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
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from concurrency.exceptions import RecordModifiedError
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class NomenclatureImportView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Импорт прайса для выбранной номенклатуры"""
    template_name = 'nomenclature/list.html'
    form_class = NomenclatureImportForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

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


class NomenclaturesServiceListView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'nomenclature/list.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        context['marks'] = MARK_CHOICES
        context['nomenclatures'] = NomenclatureService.get_nomenclatures_by_tradepoint_id(self.kwargs['tpID'])
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        context = self.get_context_data()

        if request.GET.get('nomID'):
            context['nomID'] = int(request.GET.get('nomID'))

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


class NomenclatureCreate(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'nomenclature/nomenclature_create.html'
    form_class = NomenclatureForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

    def post(
            self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse or HttpResponseRedirect:
        form = self.form_class(request.POST)

        if form.is_valid():
            nomenclature = NomenclatureService.create_nomenclature(form.cleaned_data)
            cache.delete('nomenclatures')

            tradepoint = TradePointServices.get_trade_point_by_id({'tpID': self.kwargs['tpID']})
            tradepoint.nomenclature.add(nomenclature)

            response = redirect('nomenclature_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])
            response['Location'] += f'?nomID={nomenclature.id}'

            return response

        context = self.get_context_data()
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )
        context['form'] = form

        return render(request, self.template_name, context)


class NomenclatureExportView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Экспорт прайса по выбранной номенклатуре"""
    template_name = 'nomenclature/list.html'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

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


class NomenclatureDownloadView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """При удачном выполнении задачи выдает загруженный файл"""
    template_name = 'nomenclature/list.html'
    services_file = ''

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

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
            request.session['error'] = 'Проверьте наличие прайсов у номенклатуры, или наличие номенклатуры'
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
                nom_name=str(picked_nomenclature)
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
            data=self.exel_form, file_extension=extension, nom_name=''
        )


class NomenclatureProgressView(ResetOrderCreateFormDataMixin, LoginRequiredMixin, TemplateView):
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


class NomenclatureNameUpdateApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NomenclatureUpdateSerializer

    def get(self, request, *args, **kwargs):
        nomenclature = NomenclatureService.get_nomenclature_by_id(self.kwargs.get('pk'))
        serializer = NomenclatureUpdateSerializer(nomenclature)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        nomenclature = NomenclatureService.get_nomenclature_by_id(self.kwargs.get('pk'))
        serializer = NomenclatureUpdateSerializer(nomenclature, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except RecordModifiedError:
                nomenclature = NomenclatureService.get_nomenclature_by_id(self.kwargs.get('pk'))
                return Response({
                    'current_data': {'name': nomenclature.name},
                    'new_data': {'name': request.data['name']},
                    'error': 'Наименование номенклатуры было изменено другим пользователем! Вы хотите повторно изменить наименование?'
                })
            else:
                return Response(serializer.data)
        return Response(serializer.errors)


class NomenclatureNameConcurrencyUpdateApiView(GenericAPIView):
    serializer_class = NomenclatureUpdateSerializer

    def patch(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        nomenclature = NomenclatureService.get_nomenclature_by_id(self.kwargs.get('pk'))

        with disable_concurrency(nomenclature):
            nomenclature.name = request.data['name']
            nomenclature.save()

            return Response({
                'name': nomenclature.name,
                'version': nomenclature.version
            })

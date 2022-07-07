import json
import uuid
from typing import List
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from services.report_services import ReportService
from .forms import ReportDateForm, ReportDownloadForm
from django.shortcuts import render
import datetime
import calendar
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from services.employee_services import EmployeeServices

from django.conf import settings
from rest_framework.generics import GenericAPIView
import redis
from rest_framework.response import Response


class ReportListView(TemplateView):
    template_name = 'report/report_list.html'


class ReportRedisView(GenericAPIView):
    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
        count = 0
        items = []

        for key in redis_instance.keys('*'):
            items.append(json.loads(redis_instance.get(key)))
            count += 1

        items = sorted(items, key=lambda d: d['created_at'], reverse=True)
        response = {
            'msg': f'Найдено элементов: {count}',
            'items': items,
        }
        return Response(response)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        data = request.data
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

        report_uuid = str(uuid.uuid4())

        report = {
            'uuid': report_uuid,
            'report': json.loads(data['report']),
            'created_at': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
            'from_date':  data['from_date'],
            'to_date':  data['from_date'],
        }

        redis_instance.set(report_uuid, json.dumps(report), 604800)

        response = {
            'msg': 'success'
        }

        return Response(response)


class ReportPreviewView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'report/report.html'
    form_class = ReportDateForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_default_date(self) -> List[str]:
        current_date = datetime.date.today()
        current_year = current_date.year
        current_month = current_date.month

        from_date = datetime.date(
            current_year,
            current_month,
            1
        )
        to_date = datetime.date(
            current_year,
            current_month,
            calendar.monthrange(current_year, current_month)[1]
        )

        return [str(from_date), str(to_date)]

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        initial = {}
        initial['from_date'], initial['to_date'] = self.get_default_date()

        form = self.form_class(initial)

        context = self.get_context_data(**kwargs)
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['from_date'] = form.cleaned_data['from_date']
            context['to_date'] = form.cleaned_data['to_date']

            return render(request, self.template_name, context)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form

            return render(request, self.template_name, context)


class ReportDownloadView(TemplateView):
    """При удачном выполнении задачи выдает загруженный файл отчёта"""
    template_name = 'report/report.html'
    reports_file = ''
    form_class = ReportDownloadForm

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['orgID'] = self.kwargs['orgID']
        context['tpID'] = self.kwargs['tpID']
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        form = self.form_class(data=request.POST)
        self.get_context_data(**self.kwargs)
        if form.is_valid():
            extension = request.POST['format']
            if request.POST['data']:
                main_data = json.loads(request.POST['data'])
                self.reports_file = ReportService.download_a_exel_file_to_user(
                    file_data=main_data,
                    file_extension=extension
                )
                return self.reports_file
            else:
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return render(request, template_name=self.template_name, context=context)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, template_name=self.template_name, context=context)

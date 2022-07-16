import json
import os
import uuid
from typing import List, Dict, Any
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import TemplateView

from models.report.models import Report
from services.report_services import ReportService
from .forms import ReportDateForm, ReportDownloadForm
from django.shortcuts import redirect, render
import datetime
import calendar
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from services.employee_services import EmployeeServices
from celery.result import AsyncResult
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .tasks import upload_report_to_bucket
import boto3


class ReportDetailView(TemplateView):
    template_name = 'report/report_detail.html'

    def get_report(self, repUID: str) -> Dict[str, Any]:
        report = Report.objects.get(report_uuid=repUID)

        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        result = client.get_object(Bucket=os.environ.get('AWS_BUCKET_NAME'), Key=f'report {report.report_uuid}')

        report_from_aws = json.loads(result["Body"].read().decode())
        report_from_aws['from_date'] = datetime.datetime.strptime(
            report_from_aws['from_date'], '%Y-%m-%d'
        ).strftime('%d.%m.%Y')
        report_from_aws['to_date'] = datetime.datetime.strptime(
            report_from_aws['to_date'], '%Y-%m-%d'
        ).strftime('%d.%m.%Y')

        return report_from_aws

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['report'] = self.get_report(self.kwargs['repUID'])
        context['tpID'] = self.kwargs['tpID']

        return context


class ReportListView(TemplateView):
    template_name = 'report/report_list.html'


class ReportCreateAwsApiView(GenericAPIView):
    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        data = request.data

        report = {
            'uuid': str(uuid.uuid4()),
            'report': json.loads(data['report']),
            'created_at': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
            'from_date':  data['from_date'],
            'to_date':  data['from_date'],
            'tradepoint_id': self.kwargs['tpID']
        }

        task = upload_report_to_bucket.delay(report)
        result = AsyncResult(task.id).get()

        if result:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error'})


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
                    file_data=main_data, file_extension=extension)
                return self.reports_file
            else:
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return render(request, template_name=self.template_name, context=context)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, template_name=self.template_name, context=context)


class ReportDeleteView(View):
    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        report = Report.objects.get(report_uuid=self.kwargs['repUID'])

        client = boto3.client('s3')
        client.delete_object(
            Bucket=os.environ.get('AWS_BUCKET_NAME'),
            Key=f'report {report.report_uuid}'
        )

        report.delete()

        return redirect('report_list', orgID=self.kwargs['orgID'], tpID=self.kwargs['tpID'])

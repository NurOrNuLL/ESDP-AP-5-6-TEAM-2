from typing import List
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from .forms import ReportDateForm
from django.shortcuts import render
import datetime
import calendar


class ReportPreviewView(TemplateView):
    template_name = 'report/report.html'
    form_class = ReportDateForm

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

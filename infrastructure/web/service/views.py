import json
from django.views.generic import TemplateView
from .forms import ServiceImportForm
from django.shortcuts import redirect, render
import excel2json
from models.nomenclature.models import Nomenclature
import pandas


class ServiceImportView(TemplateView):
    template_name = 'service/import_export.html'
    form_class = ServiceImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomenclatures'] = Nomenclature.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = pandas.read_excel(form.cleaned_data['excel_file'])
            json_data = json.loads(data.to_json(orient='records'))
            nomenclature = Nomenclature.objects.get(id=form.cleaned_data['nomenclature_id'])
            nomenclature.services = json_data

            return redirect('home', orgID=self.kwargs['orgID'])
        else:
            context = self.get_context_data()
            context['form'] = form

            return render(self.request, template_name=self.template_name, context=context)


class ServiceListView(TemplateView):
    template_name = 'service/list.html'


class ServiceExportView(TemplateView):
    """Экспортировать услуги"""
    template_name = 'service/import.html'

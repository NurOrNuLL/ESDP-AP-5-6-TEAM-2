from django.views.generic import TemplateView


class ServiceImportView(TemplateView):
    template_name = 'service/import_export.html'


class ServiceListView(TemplateView):
    template_name = 'service/list.html'


class ServiceExportView(TemplateView):
    """Экспортировать услуги"""
    template_name = 'service/import.html'

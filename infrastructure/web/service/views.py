import tablib
from django.forms import model_to_dict
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from urllib.parse import urlencode
from django.db.models import Q
from django.shortcuts import redirect, render

from models.nomenclature.models import Nomenclature
from .forms import FilterForm, ServiceImportForm
from models.service.admin import ServiceResource
from tablib import Dataset
from models.service.models import Service
from models.service.category_choices import CATEGORY_CHOICES, MARK_CHOICES
from django.shortcuts import get_object_or_404


class ServiceImportView(TemplateView):
    template_name = 'service/import_export.html'
    resource_class = ServiceResource
    form_class = ServiceImportForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        dataset = Dataset(headers=('Номенклатура', 'Название', 'Категория', 'Марка', 'Примечание', 'Цена'))
        resource = self.resource_class()

        if form.is_valid():
            dataset.load(form.cleaned_data.get('excel_file').read())
            result = resource.import_data(dataset, dry_run=True)

            if result.has_errors():
                error_messeage = "Некоректный документ. Проверьте в нем наличие полей: " \
                                 "Номенклатура, Название, Категория, Марка, Примечание, Цена"
                return render(
                    request=request,
                    template_name=self.template_name,
                    context={'error': error_messeage},
                )
            else:
                resource.import_data(dataset, dry_run=False)

        return redirect('home', orgID=self.kwargs['orgID'])


class ServiceListView(ListView):
    template_name = 'service/list.html'
    model = Service
    context_object_name = 'services'
    paginate_by = 15

    def get_filter_form(self):
        return FilterForm(self.request.GET)

    def get_filter_value(self):
        if self.form.is_valid():
            search = self.form.cleaned_data.get('search')
            category = self.form.cleaned_data.get('category')
            mark = self.form.cleaned_data.get('mark')
            filter_values = {
                "search": search,
                "category": category,
                "mark": mark,
            }
            return filter_values

    def get(self, request, *args, **kwargs):
        self.form = self.get_filter_form()
        self.filter_values = self.get_filter_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['categories'] = CATEGORY_CHOICES
        context['mark'] = MARK_CHOICES
        if self.filter_values:
            context['query'] = urlencode(
                {'search': self.filter_values['search'],
                 'category': self.filter_values['category'],
                 'mark': self.filter_values['mark']})
            context['search'] = self.filter_values['search']
            context['category'] = self.filter_values['category']
            context['mark'] = self.filter_values['mark']
        return context

    def get_queryset(self):
        if self.filter_values:
            query = (Q(name__icontains=self.filter_values.get('search'))
                     & Q(category__icontains=self.filter_values.get('category'))
                     & Q(mark__icontains=self.filter_values.get('mark'))) # noqa E501
            queryset = self.model.objects.filter(query)
            return queryset
        return self.model.objects.all()


class ServiceExportView(TemplateView):
    """Экспортировать услуги"""
    template_name = 'service/import.html'
    main_data = ''
    resource_class = ServiceResource

    def post(self, request, *args, **kwargs):
        type = request.POST.get('type')
        out_resource = list(map(model_to_dict, Service.objects.all()))
        data = tablib.Dataset(headers=['id', 'category', 'name',
                                       'note', 'mark', 'price'])
        for i in out_resource:
            data.append(i.values())
            self.main_data = data.export(type)
        if type == 'xls' or type == 'xlsx':
            context = 'application/vnd.ms-excel'
        else:
            context = 'text/csv'
        response = HttpResponse(self.main_data, content_type=context)
        response['Content-Disposition'] = f'attachment; filename="price.{type}"'
        return response

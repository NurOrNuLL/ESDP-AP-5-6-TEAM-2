from django.views.generic import TemplateView, ListView
from urllib.parse import urlencode
from django.db.models import Q
from django.shortcuts import redirect, render
from apps.web.form import SearchForm
from ...models.service.admin import ServiceResource
from apps.web.forms.service.forms import ServiceImportForm
from tablib import Dataset
from apps.web.models.service import Service


class ServiceImportView(TemplateView):
    template_name = 'service/import.html'
    resource_class = ServiceResource
    form_class = ServiceImportForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        dataset = Dataset()
        dataset.headers = ('id', 'category', 'name', 'note', 'price_category', 'price')
        resource = self.resource_class()

        if form.is_valid():
            dataset.load(form.cleaned_data.get('excel_file').read())
            result = resource.import_data(dataset, dry_run=True)

            if result.has_errors():
                error_messeage = "Некоректный документ. Проверьте в нем наличие полей: " \
                                 "id, category, name, note, price_category, price"
                return render(
                    request=request,
                    template_name=self.template_name,
                    context={'error': error_messeage}
                )
            else:
                services = Service.objects.all().delete()
                print(services)
                resource.import_data(dataset, dry_run=False)
        return redirect('home')


class ServiceListView(ListView):
    template_name = 'service/service_list.html'
    model = Service
    context_object_name = 'services'
    ordering = ('name', 'category', 'price_category')

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = (Q(category__icontains=self.search_value)
                     | Q(name__icontains=self.search_value)
                     | Q(price_category__icontains=self.search_value))
            queryset = queryset.filter(query)
        return queryset

                return redirect('home')

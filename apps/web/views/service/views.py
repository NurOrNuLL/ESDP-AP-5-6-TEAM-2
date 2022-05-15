from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from ...models.service.admin import ServiceResource
from ...forms.service.forms import ServiceImportForm
from ...models.service.models import Service
from tablib import Dataset


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
                error_messeage = 'Некоректный документ. Проверьте в нем наличие полей: id, category, name, note, price_category, price'
                return render(request=request, template_name=self.template_name, context={'error': error_messeage})
            else:
                services = Service.objects.all().delete()
                print(services)
                resource.import_data(dataset, dry_run=False)
                return redirect('home')

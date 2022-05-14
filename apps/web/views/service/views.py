from django.views.generic import TemplateView
from django.shortcuts import redirect
from ...models.service.admin import ServiceResource
from ...forms.service.forms import ServiceImportForm
from tablib import Dataset


class ServiceImportView(TemplateView):
    template_name = 'service/import.html'
    resource_class = ServiceResource
    form_class = ServiceImportForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        dataset = Dataset()
        resource = self.resource_class()

        if form.is_valid():
            dataset.load(form.cleaned_data.get('excel_file').read())
            result = resource.import_data(dataset, dry_run=True)

            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)

        return redirect('home')

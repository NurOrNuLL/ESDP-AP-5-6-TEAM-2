from django.views.generic import TemplateView
from .forms import NomenclatureForm
from django.shortcuts import render, redirect
from services.nomenclature_services import create_nomenclature


class NomenclatureCreate(TemplateView):
    template_name = 'nomenclature/nomenclature_create.html'
    form_class = NomenclatureForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            create_nomenclature(form.cleaned_data)
            return redirect('home', orgID=1)

        return render(request, self.template_name, {'form': form})

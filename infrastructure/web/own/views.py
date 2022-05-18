from django.views.generic import TemplateView
from .forms import OwnForm
from django.shortcuts import render, redirect
from services.own_services import create_own


class OwnCreate(TemplateView):
    template_name = 'own/own_create.html'
    form_class = OwnForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            create_own(form.cleaned_data, contractor_id=self.kwargs.get('contrID'))
            return redirect('home', orgID=1)

        return render(request, self.template_name, {'form': form})

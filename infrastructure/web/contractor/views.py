from django.views.generic import TemplateView
from .forms import ContractorForm
from django.shortcuts import render, redirect
from services.contractor_services import create_contractor


class ContractorCreate(TemplateView):
    template_name = 'contractor/contractor_create.html'
    form_class = ContractorForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            create_contractor(form.cleaned_data)
            return redirect('home', orgID=1)

        return render(request, self.template_name, {'form': form})

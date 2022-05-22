from django.views.generic import TemplateView
from .forms import ContractorForm
from django.shortcuts import render, redirect
from services.contractor_services import create_contractor, \
    get_contractors, get_contractor_by_id
from services.organization_services import get_organization_by_id


class ContractorCreate(TemplateView):
    template_name = 'contractor/contractor_create.html'
    form_class = ContractorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = get_organization_by_id(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            trust_person = dict(name=request.POST['trust_person_name'],
                                comment=request.POST['trust_person_comment'])
            form.cleaned_data['trust_person'] = trust_person
            contractor = create_contractor(form.cleaned_data)
            return redirect('contractor_detail',
                            orgID=self.kwargs['orgID'], contrID=contractor.pk)
        return render(request, self.template_name, {'form': form})


class ContractorList(TemplateView):
    template_name = 'contractor/contractors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contractors'] = get_contractors(kwargs)
        context['organization'] = get_organization_by_id(kwargs)
        return context


class ContractorDetail(TemplateView):
    template_name = 'contractor/contractor_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contractor'] = get_contractor_by_id(kwargs)
        context['organization'] = get_organization_by_id(kwargs)
        return context

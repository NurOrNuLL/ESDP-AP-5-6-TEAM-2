import json

from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import EmployeeForm
from services.employee_services import EmployeeServices
from .tasks import upload


class EmployeeCreate(TemplateView):
    template_name = 'employee/employee_create.html'
    form_class = EmployeeForm
    initial_data = {
        'role': 'Мастер'
    }

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        context = self.get_context_data(**kwargs)
        context['tradepoints'] = EmployeeServices.get_tradepoint()

        context['roles'] = self.initial_data
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            local_path = '/home/asparukh/Desktop/super_sto/ESDP-AP-5-6-TEAM-2/image/' + str(form.cleaned_data['image'])
            path = 'image/' + str(form.cleaned_data['image'])
            task = upload.apply_async(args=[local_path, path], ignore_result=True)
            EmployeeServices.create_employee(form.cleaned_data)
            return HttpResponse(json.dumps({"task_id": task.id}), content_type='application/json')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['roles'] = self.initial_data
            context['tradepoints'] = EmployeeServices.get_tradepoint()
            return render(request, self.template_name, context)

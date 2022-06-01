from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import EmployeeForm
from services.employee_services import EmployeeServices


class EmployeeCreate(TemplateView):
    template_name = 'employee/employee_create.html'
    form_class = EmployeeForm

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        context = self.get_context_data(**kwargs)
        context['role'] = EmployeeServices.get_employee()
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            EmployeeServices.create_employee(form.cleaned_data)
            return redirect('home', orgID=1)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['role'] = EmployeeServices.get_employee()
            return render(request, self.template_name, context)

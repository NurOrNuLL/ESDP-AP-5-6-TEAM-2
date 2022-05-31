from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from .forms import RegisterForm
from infrastructure.web.employee.forms import EmployeeForm


class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    register_form_class = RegisterForm
    employee_form_class = EmployeeForm

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        post_data = request.POST

        register_data = {
            'username': post_data.pop('username'),
            'password': post_data.pop('password'),
            'password_confirm': post_data.pop('password_confirm')
        }

        employee_data = post_data

        register_form = self.register_form_class(data=register_data)
        employee_form = self.employee_form_class(data=employee_data)

        if register_form.is_valid() and employee_form.is_valid():
            register_form.save()
            employee_form.save()

            return redirect('home', orgID=self.kwargs['orgID'])
        else:
            context = self.get_context_data()
            context['register_form'] = register_form
            context['employee_form'] = employee_form

            return render(request=request, template_name=self.template_name, context=context)

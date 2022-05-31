from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from .forms import RegisterForm
from infrastructure.web.employee.forms import EmployeeForm
from typing import Dict, Any
from models.trade_point.models import TradePoint
from models.employee.models import Employee


class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    register_form_class = RegisterForm
    employee_form_class = EmployeeForm

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['roles'] = [('Управляющий', 'Управляющий'), ('Менеджер', 'Менеджер')]
        context['tradepoints'] = TradePoint.objects.all()

        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        post_data = request.POST.copy()

        register_data = {
            'username': post_data.pop('username')[0],
            'password': post_data.pop('password'),
            'password_confirm': post_data.pop('password_confirm')
        }

        employee_data = post_data

        register_form = self.register_form_class(data=register_data)
        employee_form = self.employee_form_class(employee_data, request.FILES)

        if register_form.is_valid() and employee_form.is_valid():
            user = register_form.save()
            Employee.objects.create(
                uuid=user.uuid,
                name=employee_form.cleaned_data['name'],
                surname=employee_form.cleaned_data['surname'],
                role=employee_form.cleaned_data['role'],
                IIN=employee_form.cleaned_data['IIN'],
                pdf=employee_form.cleaned_data['pdf'],
                address=employee_form.cleaned_data['address'],
                phone=employee_form.cleaned_data['phone'],
                birthdate=employee_form.cleaned_data['birthdate'],
                tradepoint=employee_form.cleaned_data['tradepoint']
            )

            return redirect('home', orgID=self.kwargs['orgID'])
        else:
            context = self.get_context_data()
            context['register_form'] = register_form
            context['employee_form'] = employee_form

            return render(request=request, template_name=self.template_name, context=context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'next': request.GET.get('next')
        }
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_page = request.GET.get('next')
        if user is not None:
            login(request, user)
            if next_page:
                return redirect(next_page)
            return redirect('home', orgID=1)
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('login', orgID=1)

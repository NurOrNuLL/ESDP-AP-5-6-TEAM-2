import json

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse

from services.employee_services import EmployeeServices
from .forms import RegisterForm
from infrastructure.web.employee.forms import EmployeeForm
from typing import Dict, Any
from services.trade_point_services import TradePointServices
from infrastructure.web.employee.tasks import upload


class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    register_form_class = RegisterForm
    employee_form_class = EmployeeForm

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['roles'] = [('Управляющий', 'Управляющий'), ('Менеджер', 'Менеджер')]
        context['tradepoints'] = TradePointServices.get_trade_points(self.kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(
            self.request, self.request.user.uuid
        )

        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        post_data = request.POST.copy()

        register_data = {
            'username': post_data.pop('username')[0],
            'password': post_data.pop('password')[0],
            'password_confirm': post_data.pop('password_confirm')[0]
        }

        employee_data = post_data

        register_form = self.register_form_class(data=register_data)
        employee_form = self.employee_form_class(employee_data, request.FILES)

        if register_form.is_valid() and employee_form.is_valid():
            local_path = '/home/asparukh/Desktop/super_sto/ESDP-AP-5-6-TEAM-2/image/' + \
                         str(employee_form.cleaned_data['image'])
            path = 'image/' + str(employee_form.cleaned_data['image'])
            user = register_form.save()
            task = upload.apply_async(args=[local_path, path], ignore_result=True)
            EmployeeServices.create_employee_with_uuid(
                user.uuid, employee_form.cleaned_data
            )

            return HttpResponse(json.dumps(
                {"task_id": task.id}), content_type='application/json'
            )
        else:
            context = self.get_context_data()
            context['register_form'] = register_form
            context['employee_form'] = employee_form

            return render(
                request=request, template_name=self.template_name, context=context
            )


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
            return redirect('home_redirect')
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('login')

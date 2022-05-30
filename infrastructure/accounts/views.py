from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


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

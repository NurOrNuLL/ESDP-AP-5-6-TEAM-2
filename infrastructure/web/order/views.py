from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import render, redirect
from models.trade_point.models import TradePoint
from services.employee_services import EmployeeServices

from infrastructure.web.trade_point.context_processor import trade_point_context
from typing import Dict, Any
from django.http import HttpRequest, HttpResponse


class HomePageView(TemplateView):
    template_name = 'home.html'
    trade_points = trade_point_context(request)

    def get_context_data(self, **kwargs: dict) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tpID'] = EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid)

        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        return render(request, self.template_name, self.get_context_data())


class HomeRedirectView(View):
    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        return redirect('home', orgID=1, tpID=EmployeeServices.get_attached_tradepoint_id(self.request, self.request.user.uuid))

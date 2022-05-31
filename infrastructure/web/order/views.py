from django.template.context_processors import request
from django.views.generic import TemplateView

from infrastructure.web.trade_point.context_processor import trade_point_context


class HomePageView(TemplateView):
    template_name = 'home.html'
    trade_points = trade_point_context(request)

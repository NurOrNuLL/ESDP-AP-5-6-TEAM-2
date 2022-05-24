from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import TradePointForm
from services.trade_point_services import create_trade_point
from models.nomenclature.models import Nomenclature


class TradePointCreate(TemplateView):
    template_name = 'trade_point/trade_point_create.html'
    form_class = TradePointForm
    # extra_context = {'nomenclature': Nomenclature.objects.all()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomenclature'] = Nomenclature.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():
            create_trade_point(form.cleaned_data)
            return redirect('home', orgID=1)

        return render(request, self.template_name, {
            'form': form,
            'nomenclature': Nomenclature.objects.all()
        })

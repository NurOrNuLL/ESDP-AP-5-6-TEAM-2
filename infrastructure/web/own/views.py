from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from services.own_services import OwnServices
from .forms import OwnForm
from rest_framework.generics import GenericAPIView
from .serializer import OwnSerializer
from rest_framework.response import Response
import json
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse


class OwnCreate(TemplateView):
    template_name = 'own/own_create.html'
    form_class = OwnForm

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            OwnServices.create_own(form.cleaned_data, contractor_id=self.kwargs.get('contrID'))
            return redirect(
                'contractor_detail', orgID=self.kwargs.get('orgID'),
                contrID=self.kwargs.get('contrID')
            )

        return render(request, self.template_name, {'form': form})


class OwnDeleteView(GenericAPIView):
    serializer_class = OwnSerializer

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> JsonResponse:
        data = json.loads(request.body)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            OwnServices.delete_own(serializer.data.get('own_id'))
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

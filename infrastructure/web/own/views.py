import json
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from services.own_services import OwnServices
from .forms import OwnForm
from rest_framework.generics import GenericAPIView
from .serializer import OwnSerializer, OwnIdSerializer
from rest_framework.response import Response
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
                contrID=self.kwargs.get('contrID'),
                tpID=self.kwargs['tpID']
            )

        return render(request, self.template_name, {'form': form})


class OwnDeleteView(GenericAPIView):
    serializer_class = OwnIdSerializer

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> JsonResponse:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            OwnServices.delete_own(serializer.data.get('own_id'))
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class OwnList(GenericAPIView):
    serializer_class = OwnSerializer

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> JsonResponse:
        owns = OwnServices.get_own_by_contr_id(request.GET['contrID'])
        serializer = self.serializer_class(owns, many=True)

        return Response(serializer.data)

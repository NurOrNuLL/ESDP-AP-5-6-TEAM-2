from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from services.own_services import create_own, delete_own
from .forms import OwnForm
from rest_framework.generics import GenericAPIView
from .serializer import OwnSerializer
from rest_framework.response import Response
import json


class OwnCreate(TemplateView):
    template_name = 'own/own_create.html'
    form_class = OwnForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            create_own(form.cleaned_data, contractor_id=self.kwargs.get('contrID'))
            return redirect(
                'contractor_detail', orgID=self.kwargs.get('orgID'),
                contrID=self.kwargs.get('contrID')
            )

        return render(request, self.template_name, {'form': form})


class OwnDeleteView(GenericAPIView):
    serializer_class = OwnSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            delete_own(serializer.data.get('own_id'))
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

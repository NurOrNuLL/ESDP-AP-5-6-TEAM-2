from concurrency.api import disable_concurrency
from concurrency.exceptions import RecordModifiedError
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.permissions import AllowAny

from services.organization_services import OrganizationService
from services.own_services import OwnServices
from .forms import OwnForm
from rest_framework.generics import GenericAPIView
from .serializer import OwnSerializer, OwnIdSerializer, OwnUpdateSerializer
from rest_framework.response import Response
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from infrastructure.web.order.helpers import ResetOrderCreateFormDataMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from services.employee_services import EmployeeServices


class OwnCreate(ResetOrderCreateFormDataMixin, UserPassesTestMixin, TemplateView):
    template_name = 'own/own_create.html'
    form_class = OwnForm

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            employee = EmployeeServices.get_employee_by_uuid(self.request.user.uuid)
            return employee.role == 'Управляющий' and employee.tradepoint_id == self.kwargs.get('tpID')

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['organization'] = OrganizationService.get_organization_by_id(self.kwargs)
        context['tpID'] = self.kwargs['tpID']
        return context

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.delete_order_data_from_session(request)

        return super().get(request, *args, **kwargs)

    def post(
            self, request: HttpRequest,
            *args: list, **kwargs: dict
    ) -> HttpResponseRedirect or HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            if form.cleaned_data['number']:
                if ' ' in form.cleaned_data['number']:
                    clean_number_string = form.cleaned_data['number'].replace(' ', '')
                    form.cleaned_data['number'] = clean_number_string.upper()
                form.cleaned_data['number'] = form.cleaned_data['number'].upper()
            else:
                if not form.cleaned_data['is_part']:
                    form.errors.number = 'Обязательное поле!'

                    context = self.get_context_data(**kwargs)
                    context['form'] = form

                    return render(request, template_name=self.template_name, context=context)


            own = OwnServices.create_own(
                form.cleaned_data,
                contractor_id=self.kwargs.get('contrID')
            )

            if request.GET.get('next'):
                request.session['contractor'] = self.kwargs['contrID']
                request.session['own'] = own.id

                return redirect(
                    request.GET.get('next'),
                    orgID=self.kwargs.get('orgID'),
                    tpID=self.kwargs['tpID']
                )
            else:
                return redirect(
                    'contractor_detail',
                    orgID=self.kwargs.get('orgID'),
                    tpID=self.kwargs['tpID'],
                    contrID=self.kwargs.get('contrID')
                )

        if not form.cleaned_data['is_part']:
            form.errors.number = 'Обязательное поле!'

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, template_name=self.template_name, context=context)


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


class OwnFullList(LoginRequiredMixin, TemplateView):
    template_name = 'own/owns.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owns'] = OwnServices.get_owns()
        context['tpID'] = self.kwargs['tpID']
        context['organization'] = OrganizationService.get_organization_by_id(kwargs)
        return context


class MyPagination(PageNumberPagination):
    page_size = 100


class OwnFilterApiView(generics.ListAPIView):
    serializer_class = OwnSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['is_part']
    search_fields = ['name', 'number', 'comment']
    pagination_class = MyPagination
    queryset = OwnServices.get_owns()


class OwnUpdateApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OwnUpdateSerializer

    def get(self, request, *args, **kwargs):
        own = OwnServices.get_own_by_id(self.kwargs.get('ownID'))

        serializer = OwnSerializer(own)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        own = OwnServices.get_own_by_id(self.kwargs.get('ownID'))
        serializer = self.serializer_class(own, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except RecordModifiedError:
                own = OwnServices.get_own_by_id(self.kwargs.get('ownID'))
                return Response({
                    'current_data': {'name': own.name,
                                     'number': own.number,
                                     'comment': own.comment},
                    'new_data': {'name': request.data['name'],
                                 'number': request.data['number'],
                                 'comment': request.data['comment'],
                                 },
                    'error': 'Наименование собственности было изменено другим пользователем! Вы хотите повторно изменить наименование?'
                })
            else:
                own.name = serializer.data['name']
                own.number = serializer.data['number']
                own.comment = serializer.data['comment']
                own.save()

                return Response(serializer.data)
        return Response(serializer.errors)


class OwnConcurrencyUpdateApiView(GenericAPIView):
    serializer_class = OwnUpdateSerializer

    def patch(self, request: HttpRequest, *args: list, **kwargs: dict) -> Response:
        own = OwnServices.get_own_by_id(self.kwargs.get('ownID'))
        print(request)
        with disable_concurrency(own):
            own.name = request.data['name']
            own.number = request.data['number']
            own.comment = request.data['comment']
            own.save()

            return Response(request.data)

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from .order.views import (
    HomePageView, OrderCreateFromContractor,
    OrderDetail, OrderCreateViewStage1,
    OrderCreateViewStage2, OrderCreateViewStage3,
    OrderCreateViewStage4, OrderUpdateView,
    OrderUpdateConcurrencyView, OrderListApiView
)
from .nomenclature.views import (
    NomenclatureCreate, NomenclatureImportView,
    NomenclaturesServiceListView,
    NomenclatureItemsFilterApiView,
    NomenclatureExportView,
    NomenclatureFormForImpost,
    NomenclatureDownloadView,
    NomenclatureProgressView
)
from .own.views import OwnDeleteView, OwnCreate, OwnList

from .trade_point.views import TradePointCreate, TradePointList, \
    TradePointUpdate, TradePointUpdateConcurrecnyView

from .contractor.views import (ContractorCreate, ContractorList, ContractorDetail,
                               ContractorUpdate, ContractorFilterApiView,
                               ContractorUpdateConcurrecnyView)

from .employee.views import (EmployeeCreate,
                             EmployeeFilterApiView, EmployeeList, EmployeeDetail, EmployeeUpdate,
                             EmployeeConcurrencyUpdate, EmployeeImageUpdateView)
from infrastructure.accounts.views import RegisterView

from infrastructure.web.report.views import ReportCreateView, ReportPreviewView

nomenclature_urls = [
    path(
        'nomenclature/export/',
        NomenclatureExportView.as_view(),
        name='nomenclature_export'
    ),
    path("celery-progress/", NomenclatureProgressView.as_view(), name="progress"),
    path(
        'nomenclature/export/download/',
        NomenclatureDownloadView.as_view(),
        name='nomenclature_download'
    ),
    path(
        'nomenclature/form_import/',
        NomenclatureFormForImpost.as_view(), name='nomenclature_form_import'
    ),
    path(
        'nomenclature/import/',
        NomenclatureImportView.as_view(), name="nomenclature_import"
    ),
    path('nomenclature/create/', NomenclatureCreate.as_view(), name="nomenclature_create"),
    path(
        'nomenclature/<int:id>/services/filter/',
        NomenclatureItemsFilterApiView.as_view()
    ),
    path(
        'nomenclature/list/', NomenclaturesServiceListView.as_view(),
        name="nomenclature_list"
    ),
]

trade_point_urls = [
    path('trade_point/create/', TradePointCreate.as_view(), name="trade_point_create"),
    path('trade_point/list/', TradePointList.as_view(), name='trade_point_list'),
    path('trade_point/<int:trade_pointID>/update/',
         TradePointUpdate.as_view(), name='trade_point_update'),
    path('trade_point/<int:trade_pointID>/update_concurrency/',
         TradePointUpdateConcurrecnyView.as_view(), name='trade_point_update_concurrency')
]

contractor_urls = [
    path('contractor/create/', ContractorCreate.as_view(), name="contractor_create"),
    path('contractor/list/', ContractorList.as_view(), name="contractors"),
    path('contractor/<int:contrID>/',ContractorDetail.as_view(), name="contractor_detail"),
    path('contractor/list/filter/', ContractorFilterApiView.as_view()),
    path('contractor/<int:contrID>/update/', ContractorUpdate.as_view(), name="contractor_update"),
    path('contractor/<int:contrID>/update_concurrency/', ContractorUpdateConcurrecnyView.as_view(),
         name="contractor_update_concurrency")
]

own_urls = [
    path('contractor/<int:contrID>/own/create/', OwnCreate.as_view(), name="own_create"),
    path(
        'contractor/<int:contrID>/own/<int:ownID>/delete/',
        OwnDeleteView.as_view(), name="own_delete"
    ),
    path('contractor/<int:contrID>/own/', OwnList.as_view(), name="own_list")
]

employee_urls = [

    path('employee/create/', EmployeeCreate.as_view(), name="employee_create"),
    path('employee/<slug:empUID>/update/image', EmployeeImageUpdateView.as_view(), name="employee_update_image"),
    path('employee/list/filter/', EmployeeFilterApiView.as_view()),
    path('employee/list/', EmployeeList.as_view(), name="employees"),
    path('employee/<slug:empUID>/', EmployeeDetail.as_view(), name="employee_detail"),
    path('employee/<slug:empUID>/update/', EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/<slug:empUID>/concurrency_update/', EmployeeConcurrencyUpdate.as_view(), name='employee_concurrency_update'),
    path('register/', RegisterView.as_view(), name='register')
]

order_urls = [
    path('contractor/<int:contrID>/own/<int:ownID>/order/create/',
         OrderCreateFromContractor.as_view(), name="order_create"),
    path('order/<int:ordID>/', OrderDetail.as_view(), name="order_detail"),
    path('order/<int:ordID>/update', OrderUpdateView.as_view(), name="order_update"),
    path('order/<int:ordID>/update/concurrency', OrderUpdateConcurrencyView.as_view(), name="order_update_concurrency"),
    path('order/create/stage/1/', OrderCreateViewStage1.as_view(), name='order_create_stage1'),
    path('order/create/stage/2/', OrderCreateViewStage2.as_view(), name='order_create_stage2'),
    path('order/create/stage/3/', OrderCreateViewStage3.as_view(), name='order_create_stage3'),
    path('order/create/stage/4/', OrderCreateViewStage4.as_view(), name='order_create_stage4'),
    path('order/list/filter/', OrderListApiView.as_view(), name='order_list')
]

report_urls = [
	path('report/preview/', ReportPreviewView.as_view(), name="report_preview"),
	path('report/create/', ReportCreateView.as_view(), name="report_create")
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

urlpatterns += nomenclature_urls
urlpatterns += trade_point_urls
urlpatterns += contractor_urls
urlpatterns += own_urls
urlpatterns += employee_urls
urlpatterns += order_urls
urlpatterns += report_urls

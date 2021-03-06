from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path

from django.views.generic import RedirectView
from .order.views import (
    HomePageView,
    OrderDetail, OrderCreateViewStage1,
    OrderCreateViewStage2, OrderCreateViewStage3,
    OrderCreateViewStage4,
    OrderFinishApiView, OrderUpdateView,
    OrderUpdateConcurrencyView, OrderListApiView
)
from .nomenclature.views import (
    NomenclatureCreate, NomenclatureImportView,
    NomenclaturesServiceListView,
    NomenclatureItemsFilterApiView,
    NomenclatureExportView,
    NomenclatureFormForImpost,
    NomenclatureDownloadView,
    NomenclatureProgressView,
    NomenclatureNameUpdateApiView, NomenclatureNameConcurrencyUpdateApiView
)
from .own.views import (
    OwnDeleteView, OwnCreate,
    OwnList, OwnFullList, OwnFilterApiView, OwnUpdateApiView, OwnConcurrencyUpdateApiView
)
from .queue.views import QueueCreate
from .trade_point.views import (
    TradePointCreate, TradePointList,
    TradePointUpdate, TradePointUpdateConcurrecnyView
)
from .contractor.views import (
    ContractorCreate, ContractorList, ContractorDetail,
    ContractorUpdate, ContractorFilterApiView,
    ContractorUpdateConcurrecnyView, ContractorDetailOwnListApiView
)
from .employee.views import (
    EmployeeCreate,
    EmployeeFilterApiView, EmployeeList,
    EmployeeDetail, EmployeeUpdate,
    EmployeeConcurrencyUpdate, EmployeeImageUpdateView
)
from infrastructure.accounts.views import RegisterView
from infrastructure.web.report.views import (
    ReportPreviewView, ReportDownloadView,
    ReportCreateAwsApiView, ReportListView,
    ReportDetailView, ReportDeleteView,
    ReportRemoveCacheAPIView
)
from infrastructure.web.report.consumers import ReportConsumer, ReportListConsumer
from .payment.views import OrderPayment
from infrastructure.web.order.consumers import OrderStatusUpdateTrackingConsumer


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
    path('nomenclature/<int:pk>/update/', NomenclatureNameUpdateApiView.as_view(), name='nomenclature_update'),
    path(
        'nomenclature/<int:pk>/update/concurrency/',
        NomenclatureNameConcurrencyUpdateApiView.as_view(),
        name="nomenclature_update_concurrency"
    )
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
    path('contractor/<int:contrID>/',
   ContractorDetail.as_view(), name="contractor_detail"),
    path('contractor/<int:contrID>/own/list/filter/',
   ContractorDetailOwnListApiView.as_view()),
    path('contractor/list/filter/', ContractorFilterApiView.as_view()),
    path('contractor/<int:contrID>/update/', ContractorUpdate.as_view(), name="contractor_update"),
    path('contractor/<int:contrID>/update_concurrency/', ContractorUpdateConcurrecnyView.as_view(),
         name="contractor_update_concurrency")
]

own_urls = [
    path('owns/', OwnFullList.as_view(), name="owns"),
    path('own/list/filter/', OwnFilterApiView.as_view()),
    path('contractor/<int:contrID>/own/create/', OwnCreate.as_view(), name="own_create"),
    path(
        'contractor/<int:contrID>/own/<int:ownID>/delete/',
        OwnDeleteView.as_view(), name="own_delete"
    ),
    path('contractor/<int:contrID>/own/', OwnList.as_view(), name="own_list"),
    path('own/<int:ownID>/update/', OwnUpdateApiView.as_view(), name='own_update'),
    path('own/<int:ownID>/update/concurrency/', OwnConcurrencyUpdateApiView.as_view(), name='own_update_concurrency'),
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
    path('order/<int:ordID>/', OrderDetail.as_view(), name="order_detail"),
    path('order/<int:ordID>/update/', OrderUpdateView.as_view(), name="order_update"),
    path('order/<int:ordID>/update/concurrency', OrderUpdateConcurrencyView.as_view(), name="order_update_concurrency"),
    path('order/create/stage/1/', OrderCreateViewStage1.as_view(), name='order_create_stage1'),
    path('order/create/stage/2/', OrderCreateViewStage2.as_view(), name='order_create_stage2'),
    path('order/create/stage/3/', OrderCreateViewStage3.as_view(), name='order_create_stage3'),
    path('order/create/stage/4/', OrderCreateViewStage4.as_view(), name='order_create_stage4'),
    path('order/list/filter/', OrderListApiView.as_view(), name='order_list'),
    path('order/<int:ordID>/finish/', OrderFinishApiView.as_view(), name='order_finish')
]

order_websocket_urls = [
    path('wss/order/status/update/tracking/', OrderStatusUpdateTrackingConsumer.as_asgi())
]

queue_urls = [
    path('queue/create/', QueueCreate.as_view(), name='queue_create'),
]

report_urls = [
    path('report/preview/', ReportPreviewView.as_view(), name="report_preview"),
    path('report/preview/download/', ReportDownloadView.as_view(), name="report_download"),
    path('report/save/', ReportCreateAwsApiView.as_view(), name='report_save'),
    path('report/', ReportListView.as_view(), name='report_list'),
    path('report/cache/delete/', ReportRemoveCacheAPIView.as_view(), name='report_cache_delete'),
    path('report/<slug:repUID>/', ReportDetailView.as_view(), name='report_detail'),
    path('report/<slug:repUID>/delete', ReportDeleteView.as_view(), name='report_delete')
]

report_websocket_urls = [
    path('wss/report/create/', ReportConsumer.as_asgi()),
    path('wss/report/list/', ReportListConsumer.as_asgi())
]

payment_url = [
    path('order/<int:ordID>/payment/', OrderPayment.as_view(), name='payment_create')
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

websocket_urlpatterns = []

urlpatterns += nomenclature_urls
urlpatterns += trade_point_urls
urlpatterns += contractor_urls
urlpatterns += own_urls
urlpatterns += employee_urls
urlpatterns += order_urls
urlpatterns += report_urls
urlpatterns += payment_url
urlpatterns += queue_urls

websocket_urlpatterns += report_websocket_urls
websocket_urlpatterns += order_websocket_urls

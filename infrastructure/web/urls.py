from django.urls import path
from .order.views import HomePageView
from .service.views import ServiceImportView, ServiceListView, ServiceExportView
from .nomenclature.views import NomenclatureCreate
from .own.views import OwnDeleteView, OwnCreate
from .contractor.views import ContractorCreate, ContractorList, ContractorDetail
from .trade_point.views import TradePointCreate

service_urls = [
    path('service/import/', ServiceImportView.as_view(), name="service_import"),
    path('service/list/', ServiceListView.as_view(), name="service_list"),
    path('service/export/', ServiceExportView.as_view(), name='service_export')
]

nomenclature_urls = [
    path('nomenclature/create/', NomenclatureCreate.as_view(), name="nomenclature_create")
]

trade_point_urls = [
    path('trade_point/create/', TradePointCreate.as_view(), name="trade_point_create")
]

contractor_urls = [
    path('contractor/create/', ContractorCreate.as_view(), name="contractor_create"),
    path('contractor/list/', ContractorList.as_view(), name="contractors"),
    path('contractor/<int:contrID>/', ContractorDetail.as_view(), name="contractor_detail")
]

own_urls = [
    path('contractor/<int:contrID>/own/create/', OwnCreate.as_view(), name="own_create"),
    path('contractor/<int:contrID>/own/<int:ownID>/delete/', OwnDeleteView.as_view(), name="own_delete")
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls
urlpatterns += nomenclature_urls
urlpatterns += trade_point_urls
urlpatterns += contractor_urls
urlpatterns += own_urls


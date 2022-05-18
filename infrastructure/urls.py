from django.urls import path
from .web.order.views import HomePageView
from .web.service.views import ServiceImportView, ServiceListView, ServiceExportView
from .web.nomenclature.views import NomenclatureCreate
from .web.trade_point.views import TradePointCreate

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

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls
urlpatterns += nomenclature_urls
urlpatterns += trade_point_urls

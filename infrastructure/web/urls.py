from django.urls import path
from .order.views import HomePageView
from .service.views import ServiceImportView, ServiceListView, ServiceExportView
from .nomenclature.views import NomenclatureCreate

service_urls = [
    path('service/import/', ServiceImportView.as_view(), name="service_import"),
    path('service/list/', ServiceListView.as_view(), name="service_list"),
    path('service/export/', ServiceExportView.as_view(), name='service_export')
]

nomenclature_urls = [
    path('nomenclature/create/', NomenclatureCreate.as_view(), name="nomenclature_create")
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls
urlpatterns += nomenclature_urls

from django.urls import path
from .order.views import HomePageView
from .service.views import ServiceImportView, ServiceListView, ServiceExportView
from .nomenclature.views import NomenclatureCreate
from .contractor.views import ContractorCreate
from .own.views import OwnCreate

service_urls = [
    path('service/import/', ServiceImportView.as_view(), name="service_import"),
    path('service/list/', ServiceListView.as_view(), name="service_list"),
    path('service/export/', ServiceExportView.as_view(), name='service_export')
]

nomenclature_urls = [
    path('nomenclature/create/', NomenclatureCreate.as_view(), name="nomenclature_create")
]

contractor_urls = [
    path('contractor/create/', ContractorCreate.as_view(), name="contractor_create")
]

own_urls = [
    path('contractor/<int:contrID>/own/create/', OwnCreate.as_view(), name="own_create")
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls
urlpatterns += nomenclature_urls
urlpatterns += contractor_urls
urlpatterns += own_urls

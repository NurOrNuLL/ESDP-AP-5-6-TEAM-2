from django.urls import path
from .web.order.views import HomePageView
from .web.service.views import ServiceImportView, ServiceListView, ServiceExportView

service_urls = [
    path('service/import/', ServiceImportView.as_view(), name="service_import"),
    path('service/list/', ServiceListView.as_view(), name="service_list"),
    path('service/export/', ServiceExportView.as_view(), name='service_export')
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls

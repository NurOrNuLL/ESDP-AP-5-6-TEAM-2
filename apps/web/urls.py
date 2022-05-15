from django.urls import path
from .views.home.views import HomePageView
from .views.service.views import ServiceImportView

service_urls = [
    path('service/import/', ServiceImportView.as_view(), name="service_import")
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += service_urls

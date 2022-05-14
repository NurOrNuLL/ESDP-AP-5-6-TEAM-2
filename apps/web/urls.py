from django.urls import path
from .views.home.views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

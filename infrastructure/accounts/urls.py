from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('<int:orgID>/register/', RegisterView.as_view(), name='register')
]

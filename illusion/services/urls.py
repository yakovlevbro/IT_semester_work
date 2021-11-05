from django.urls import path
from .views import create_service, update_service

urlpatterns = [
    path('create', create_service, name='create_service'),
    path('update/<int:pk>', update_service, name='update_service'),
]
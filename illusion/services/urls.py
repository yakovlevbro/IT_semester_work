from django.urls import path
from .views import create_service, update_service, search_page, service_page, create_order, create_feedback, show_price

urlpatterns = [
    path('create', create_service, name='create_service'),
    path('update/<int:pk>', update_service, name='update_service'),
    path('all', search_page, name='search_page'),
    path('all/<int:pk>', service_page, name='service_page'),

    path('all/<int:pk>/create_order', create_order, name='create_order'),
    path('all/<int:pk>/create_feedback', create_feedback, name='create_feedback'),
    path('all/<int:pk>/price', show_price, name='show_price'),



]
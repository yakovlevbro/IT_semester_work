from django.urls import path
from .views import reg_user, login_user, logout_user, customer_page

urlpatterns = [
    path('register', reg_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('home', customer_page, name='customer_page')

]
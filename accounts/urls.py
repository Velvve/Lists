from django.urls import path
from django.contrib.auth import logout
from accounts import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_login_email'),
    path('login', views.login, name='login'),
    path('logout', logout, {'next_page': '/'}, name='logout'),
]
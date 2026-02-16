from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('connect/<uuid:session_id>/', views.connect, name='connect'),
    path('sent_file/<uuid:session_id>/', views.send_from_phone, name='sent')
]
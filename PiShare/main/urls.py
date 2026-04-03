from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('connect/<uuid:session_id>/', views.connect, name='connect'),
    path('sent_file/<uuid:session_id>/', views.send_from_phone, name='sent_file'),
    path('receive-from-phone/<uuid:session_id>/', views.receive_from_phone, name='receive_from_phone'),
    path('check_receive/<uuid:session_id>/', views.check_receive, name='check_receive')
]
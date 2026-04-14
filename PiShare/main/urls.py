from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('connect/<uuid:session_id>/', views.connect, name='connect'),
    path('send_file/<uuid:session_id>/', views.send_file, name='send_file'),
    path('receive_file/<uuid:session_id>/', views.receive_file, name='receive_file'),
]



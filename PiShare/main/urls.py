from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('connect/<uuid:session_id>/', views.connect, name='connect'),
    path('send_file/<uuid:session_id>/', views.send_file, name='send_file'),
    path('receive_file/<uuid:session_id>/', views.receive_file, name='receive_file'),


    path('api/upload/<uuid:session_id>/', views.upload_file, name='upload_file'),
    path('api/download/<uuid:session_id>/<uuid:file_id>/', views.download_file, name='download_file'),
    path('delete/<uuid:session_id>/', views.delete_file, name='delete'),
]



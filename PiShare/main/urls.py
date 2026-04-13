from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('connect/<uuid:session_id>/', views.connect, name='connect'),
]



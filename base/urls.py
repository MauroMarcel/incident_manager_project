from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('acceso-denegado/', views.AccesoDenegadoView.as_view(), name='acceso-denegado'),
]
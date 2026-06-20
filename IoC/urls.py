from django.urls import path
from . import views

urlpatterns = [
    path('', views.IoCListView.as_view(), name='ioc-lista'),
    path('crear/', views.IoCCreateView.as_view(), name='ioc-crear'),
    path('<uuid:pk>/', views.IoCDetailView.as_view(), name='ioc-detalle'),
]
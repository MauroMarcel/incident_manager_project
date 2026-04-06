from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReporteHomeView.as_view(), name='reporte-home'),
    path('ficha/<uuid:pk>/', views.IncidenteFichaView.as_view(), name='incidente-ficha'),
]
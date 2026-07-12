from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReporteHomeView.as_view(), name='reporte-home'),
    path('lista/', views.ReporteListView.as_view(), name='reporte-lista'),
    path('crear/', views.ReporteCreateView.as_view(), name='reporte-crear'),
    path('<uuid:pk>/', views.ReporteDetailView.as_view(), name='reporte-detalle'),
    path('ficha/<uuid:pk>/', views.IncidenteFichaView.as_view(), name='incidente-ficha'),
]

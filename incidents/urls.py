from django.urls import path
from . import views

urlpatterns = [
    path('crear/<uuid:notificacion_pk>/', views.IncidenteCreateView.as_view(), name='incidente-crear'),
    path('<uuid:pk>/editar/<str:paso>/', views.IncidenteWizardView.as_view(), name='incidente-wizard'),
    path('', views.IncidenteListView.as_view(), name='incidente-lista'),
    path('<uuid:pk>/asignar/', views.IncidenteAsignarEspecialistaView.as_view(), name='incidente-asignar'),
    path('<uuid:pk>/', views.IncidenteDetailView.as_view(), name='incidente-detalle'),
    path('<uuid:pk>/declinar/', views.IncidenteDeclinarView.as_view(), name='incidente-declinar'),
    path('<uuid:pk>/evidencia/', views.IncidenteEvidenciaCreateView.as_view(), name='incidente-evidencia'),
    path('evidencia/<uuid:pk>/eliminar/', views.EvidenciaIncidenteDeleteView.as_view(), name='incidente-evidencia-eliminar'),
]
from django.urls import path
from . import views
from . import web_views

urlpatterns = [
    path('crear/', views.IncidenteCreateDirectView.as_view(), name='incidente-crear-directo'),
    path('crear/<uuid:notificacion_pk>/', views.IncidenteCreateView.as_view(), name='incidente-crear'),
    path('<uuid:pk>/editar/<str:paso>/', views.IncidenteWizardView.as_view(), name='incidente-wizard'),
    path('', views.IncidenteListView.as_view(), name='incidente-lista'),
    path('<uuid:pk>/asignar/', views.IncidenteAsignarEspecialistaView.as_view(), name='incidente-asignar'),
    path('<uuid:pk>/', views.IncidenteDetailView.as_view(), name='incidente-detalle'),
    path('<uuid:pk>/evidencia/', views.IncidenteEvidenciaCreateView.as_view(), name='incidente-evidencia'),
    path('<uuid:pk>/cambiar-estado/', views.IncidenteCambiarEstadoView.as_view(), name='incidente-cambiar-estado'),
    path('evidencia/<uuid:pk>/eliminar/', views.EvidenciaIncidenteDeleteView.as_view(), name='incidente-evidencia-eliminar'),
    path('<uuid:pk>/reasignar/', views.IncidenteReasignarEspecialistaView.as_view(), name='incidente-reasignar'),
    path('<uuid:pk>/mensajes/', views.IncidenteMensajesView.as_view(), name='incidente-mensajes'),
    path('<uuid:pk>/eliminar/', web_views.IncidenteDeleteView.as_view(), name='incidente-eliminar'),
    path('<uuid:pk>/restaurar/', views.IncidenteRestoreView.as_view(), name='incidente-restaurar'),
    path('eliminados/', views.IncidenteDeletedListView.as_view(), name='incidente-eliminados-lista'),
]
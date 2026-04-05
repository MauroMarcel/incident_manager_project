from django.urls import path
from . import web_views

urlpatterns = [
    # Tipo de Incidente
    path('tipos/', web_views.Tipo_IncidenteListView.as_view(), name='tipo-incidente-list'),
    path('tipos/crear/', web_views.Tipo_IncidenteCreateView.as_view(), name='tipo-incidente-create'),
    path('tipos/<uuid:pk>/editar/', web_views.Tipo_IncidenteUpdateView.as_view(), name='tipo-incidente-update'),
    path('tipos/<uuid:pk>/eliminar/', web_views.Tipo_IncidenteDeleteView.as_view(), name='tipo-incidente-delete'),

    # Incidentes
    path('', web_views.IncidenteListView.as_view(), name='incidente-list'),
    path('crear/', web_views.IncidenteCreateView.as_view(), name='incidente-create'),
    path('<uuid:pk>/', web_views.IncidenteDetailView.as_view(), name='incidente-detail'),
    path('<uuid:pk>/editar/', web_views.IncidenteUpdateView.as_view(), name='incidente-update'),
    path('<uuid:pk>/eliminar/', web_views.IncidenteDeleteView.as_view(), name='incidente-delete'),
]
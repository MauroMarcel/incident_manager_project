from django.urls import path
from . import views

urlpatterns = [
    path('crear/<uuid:notificacion_pk>/', views.IncidenteCreateView.as_view(), name='incidente-crear'),
    path('<uuid:pk>/editar/<str:paso>/', views.IncidenteWizardView.as_view(), name='incidente-wizard'),
    path('', views.IncidenteListView.as_view(), name='incidente-lista'),
    path('<uuid:pk>/asignar/', views.IncidenteAsignarEspecialistaView.as_view(), name='incidente-asignar'),
]
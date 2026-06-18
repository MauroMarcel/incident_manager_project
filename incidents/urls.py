from django.urls import path
from . import views

urlpatterns = [
    path('crear/<uuid:notificacion_pk>/', views.IncidenteCreateView.as_view(), name='incidente-crear'),
]
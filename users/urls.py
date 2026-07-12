from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.PersonaListView.as_view(), name='persona-lista'),
    path('crear/', views.PersonaCreateView.as_view(), name='persona-crear'),
    path('mi-perfil/', views.MiPerfilView.as_view(), name='mi-perfil'),
    path('<uuid:pk>/', views.PersonaDetailView.as_view(), name='persona-detalle'),
    path('<uuid:pk>/eliminar/', views.PersonaDeleteView.as_view(), name='persona-eliminar'),
    path('<uuid:pk>/activar/', views.PersonaActivarView.as_view(), name='persona-activar'),
    path('<uuid:pk>/editar/', views.PersonaUpdateView.as_view(), name='persona-editar'),
    path('<uuid:pk>/configurar-areas/', views.PersonaConfigurarAreasView.as_view(), name='persona-configurar-areas'),
]
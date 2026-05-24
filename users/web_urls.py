from django.urls import path
from . import web_views

urlpatterns = [
    # Categoria_Persona URLs
    path('categorias/', web_views.Categoria_PersonaListView.as_view(), name='categoria-list'),
    path('categorias/<uuid:pk>/', web_views.Categoria_PersonaDetailView.as_view(), name='categoria-detail'),
    path('categorias/crear/', web_views.Categoria_PersonaCreateView.as_view(), name='categoria-create'),
    path('categorias/<uuid:pk>/editar/', web_views.Categoria_PersonaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<uuid:pk>/eliminar/', web_views.Categoria_PersonaDeleteView.as_view(), name='categoria-delete'),
    
    # Cargo URLs
    path('cargos/', web_views.CargoListView.as_view(), name='cargo-list'),
    path('cargos/<uuid:pk>/', web_views.CargoDetailView.as_view(), name='cargo-detail'),
    path('cargos/crear/', web_views.CargoCreateView.as_view(), name='cargo-create'),
    path('cargos/<uuid:pk>/editar/', web_views.CargoUpdateView.as_view(), name='cargo-update'),
    path('cargos/<uuid:pk>/eliminar/', web_views.CargoDeleteView.as_view(), name='cargo-delete'),
    
    # Estado_Persona URLs
    path('estados/', web_views.Estado_PersonaListView.as_view(), name='estado-list'),
    path('estados/<uuid:pk>/', web_views.Estado_PersonaDetailView.as_view(), name='estado-detail'),
    path('estados/crear/', web_views.Estado_PersonaCreateView.as_view(), name='estado-create'),
    path('estados/<uuid:pk>/editar/', web_views.Estado_PersonaUpdateView.as_view(), name='estado-update'),
    path('estados/<uuid:pk>/eliminar/', web_views.Estado_PersonaDeleteView.as_view(), name='estado-delete'),
    
    # Persona URLs
    path('personas/', web_views.PersonaListView.as_view(), name='persona-list'),
    path('personas/<uuid:pk>/', web_views.PersonaDetailView.as_view(), name='persona-detail'),
    path('personas/crear/', web_views.PersonaCreateView.as_view(), name='persona-create'),
    path('personas/<uuid:pk>/editar/', web_views.PersonaUpdateView.as_view(), name='persona-update'),
    path('personas/<uuid:pk>/eliminar/', web_views.PersonaDeleteView.as_view(), name='persona-delete'),
]

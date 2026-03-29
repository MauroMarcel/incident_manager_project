from django.urls import path
from .web_views import (
    # Departamento
    DepartamentoListView,
    DepartamentoDetailView,
    DepartamentoCreateView,
    DepartamentoUpdateView,
    DepartamentoDeleteView,
    # Clasificacion Sistema
    ClasificacionSistemaListView,
    ClasificacionSistemaDetailView,
    ClasificacionSistemaCreateView,
    ClasificacionSistemaUpdateView,
    ClasificacionSistemaDeleteView,
    # Criticidad
    CriticidadListView,
    CriticidadDetailView,
    CriticidadCreateView,
    CriticidadUpdateView,
    CriticidadDeleteView,
)

urlpatterns = [
    # ===== URLs para DEPARTAMENTO =====
    path(
        'departamentos/',
        DepartamentoListView.as_view(),
        name='departamento-list'
    ),
    path(
        'departamentos/<uuid:pk>/',
        DepartamentoDetailView.as_view(),
        name='departamento-detail'
    ),
    path(
        'departamentos/crear/',
        DepartamentoCreateView.as_view(),
        name='departamento-create'
    ),
    path(
        'departamentos/<uuid:pk>/editar/',
        DepartamentoUpdateView.as_view(),
        name='departamento-update'
    ),
    path(
        'departamentos/<uuid:pk>/eliminar/',
        DepartamentoDeleteView.as_view(),
        name='departamento-delete'
    ),
    
    # ===== URLs para CLASIFICACION_SISTEMA =====
    path(
        'clasificaciones/',
        ClasificacionSistemaListView.as_view(),
        name='clasificacion-list'
    ),
    path(
        'clasificaciones/<uuid:pk>/',
        ClasificacionSistemaDetailView.as_view(),
        name='clasificacion-detail'
    ),
    path(
        'clasificaciones/crear/',
        ClasificacionSistemaCreateView.as_view(),
        name='clasificacion-create'
    ),
    path(
        'clasificaciones/<uuid:pk>/editar/',
        ClasificacionSistemaUpdateView.as_view(),
        name='clasificacion-update'
    ),
    path(
        'clasificaciones/<uuid:pk>/eliminar/',
        ClasificacionSistemaDeleteView.as_view(),
        name='clasificacion-delete'
    ),
    
    # ===== URLs para CRITICIDAD =====
    path(
        'criticidades/',
        CriticidadListView.as_view(),
        name='criticidad-list'
    ),
    path(
        'criticidades/<uuid:pk>/',
        CriticidadDetailView.as_view(),
        name='criticidad-detail'
    ),
    path(
        'criticidades/crear/',
        CriticidadCreateView.as_view(),
        name='criticidad-create'
    ),
    path(
        'criticidades/<uuid:pk>/editar/',
        CriticidadUpdateView.as_view(),
        name='criticidad-update'
    ),
    path(
        'criticidades/<uuid:pk>/eliminar/',
        CriticidadDeleteView.as_view(),
        name='criticidad-delete'
    ),
]

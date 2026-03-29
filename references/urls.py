from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartamentoViewSet,
    ClasificacionSistemaViewSet,
    CriticidadViewSet
)

# Crear el router y registrar los ViewSets
router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'clasificaciones', ClasificacionSistemaViewSet, basename='clasificacion_sistema')
router.register(r'criticidades', CriticidadViewSet, basename='criticidad')

# Incluir las URLs del router
urlpatterns = [
    path('', include(router.urls)),
]

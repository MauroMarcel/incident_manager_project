from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Crear el router y registrar los ViewSets
router = DefaultRouter()

# Incluir las URLs del router
urlpatterns = [
    path('', include(router.urls)),
]

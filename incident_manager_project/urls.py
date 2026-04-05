from django.contrib import admin
from django.urls import path, include
from incident_manager_project.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='referencia-home'),
    path('admin/', admin.site.urls),
    # Autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    # API REST
    path('api/', include('references.urls')),
    # Vistas Web
    path('referencias/', include('references.web_urls')),
    path('usuarios/', include('users.web_urls')),
    path('incidentes/', include('incidents.web_urls')),
]
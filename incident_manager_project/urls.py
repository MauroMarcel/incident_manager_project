from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', HomeView.as_view(), name='referencia-home'),
    path('admin/', admin.site.urls),
    # Autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    # API REST
    #path('api/', include('references.urls')),
    # Vistas Web
    #path('referencias/', include('references.web_urls')),
    #ath('usuarios/', include('users.web_urls')),
    #path('incidentes/', include('incidents.web_urls')),
    #path('reportes/', include('reports.web_urls')),
]
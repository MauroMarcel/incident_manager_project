from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('base.urls')),
    path('notifications/', include('notifications.urls')),
    path('incidentes/', include('incidents.urls')),
]
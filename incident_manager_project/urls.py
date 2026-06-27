from django.contrib import admin
from django.urls import path, include
from base import views as base_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', base_views.custom_logout, name='custom-logout'),
    path('', include('base.urls')),
    path('notifications/', include('notifications.urls')),
    path('incidentes/', include('incidents.urls')),
    path('indicadores/', include('IoC.urls')),
    path('personas/', include('users.urls')),
    path('organizacion/', include('organization.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
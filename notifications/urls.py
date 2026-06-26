from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.NotificationCreateView.as_view(), name='notification-create'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('list/', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/rechazar/', views.NotificationRechazarView.as_view(), name='notification-rechazar'),
    path('<uuid:pk>/vincular/', views.NotificationVincularView.as_view(), name='notificacion-vincular'),
    path('<uuid:pk>/evidencia/', views.NotificacionEvidenciaCreateView.as_view(), name='notificacion-evidencia'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.NotificationCreateView.as_view(), name='notification-create'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('list/', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/rechazar/', views.NotificationRechazarView.as_view(), name='notification-rechazar'),
]
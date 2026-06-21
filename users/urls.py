from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.PersonaListView.as_view(), name='persona-lista'),
    path('crear/', views.PersonaCreateView.as_view(), name='persona-crear'),
    path('<uuid:pk>/', views.PersonaDetailView.as_view(), name='persona-detalle'),
]
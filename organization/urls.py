from django.urls import path
from . import views

urlpatterns = [
    path('', views.AreaTreeView.as_view(), name='area-tree'),
    path('crear/', views.AreaCreateView.as_view(), name='area-crear'),
]
import django_filters
from .models import Notificacion
from django.contrib.auth.models import User
from django import forms


class NotificacionFilter(django_filters.FilterSet):
    usuario_notificador__exact = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name="usuario_notificador",
        lookup_expr='exact',
        label='Notificado por el usuario',
    )
    fecha_notificacion__date__gte = django_filters.DateFilter(
        field_name='fecha_notificacion',
        lookup_expr='date__gte',
        label='Fecha desde',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_notificacion__date__lte = django_filters.DateFilter(
        field_name='fecha_notificacion',
        lookup_expr='date__lte',
        label='Fecha hasta',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Notificacion
        fields = {
            'asunto': ['icontains'],
            'estado_notificacion': ['exact'],
            'area_notificacion': ['exact'],
            'incidente_asociado': ['exact']
        }
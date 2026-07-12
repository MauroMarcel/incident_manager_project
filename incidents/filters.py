import django_filters
from .models import Incidente
from users.models import Persona
from organization.models import Area
from django import forms


class IncidenteFilter(django_filters.FilterSet):
    supervisor = django_filters.ModelChoiceFilter(
        queryset=Persona.objects.filter(usuario_django__groups__name='Supervisor'),
        label='Supervisor'
    )
    especialista_asignado = django_filters.ModelChoiceFilter(
        queryset=Persona.objects.filter(usuario_django__groups__name='Especialista'),
        label='Especialista'
    )
    fecha_reportado__date__gte = django_filters.DateFilter(
        field_name='fecha_reportado',
        lookup_expr='date__gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_reportado__date__lte = django_filters.DateFilter(
        field_name='fecha_reportado',
        lookup_expr='date__lte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    areas_afectadas = django_filters.ModelMultipleChoiceFilter(
        queryset=Area.objects.all(),
        label="Area afectada",
        conjoined=False
    )

    class Meta:
        model = Incidente
        fields = {
            'estado_incidente': ['exact'],
            'especialista_asignado': ['exact'],
        }
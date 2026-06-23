import django_filters
from .models import Incidente
from users.models import Persona
from django import forms


class IncidenteFilter(django_filters.FilterSet):
    fecha_ocurrencia__date__gte = django_filters.DateFilter(
        field_name='fecha_ocurrencia',
        lookup_expr='date__gte',
        label='El incidente ocurrio por primera vez',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_reportado__date__gte = django_filters.DateFilter(
        field_name='fecha_reportado',
        lookup_expr='date__gte',
        label='Incidente reportado',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_asignacion__date__gte = django_filters.DateFilter(
        field_name='fecha_asignacion',
        lookup_expr='date__gte',
        label='Incidente asignado a especialista',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_solucion__date__gte = django_filters.DateFilter(
        field_name='fecha_solucion',
        lookup_expr='date__gte',
        label='Incidente cerrado',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    supervisor__exact = django_filters.ModelChoiceFilter(
        queryset=Persona.objects.all(),
        field_name="supervisor",
        lookup_expr='exact',
        label='Supervisado por',
    )
    especialista_asignado__exact = django_filters.ModelChoiceFilter(
        queryset=Persona.objects.all(),
        field_name="especialista_asignado",
        lookup_expr='exact',
        label='Asignado a',
    )

    class Meta:
        model = Incidente
        fields = {
            'codigo': ['exact'],
            'titulo': ['exact'],
            'area_afectada': ['exact'],
            'sistema_operativo': ['exact'],
            'peligrosidad': ['exact'],
            'subcategoria__categoria': ['exact'],
            'subcategoria': ['exact'],
            'alcance': ['exact'],
            'vector_ataque': ['exact'],
            'fuente_deteccion': ['exact'],
            'tecnologia': ['exact'],
            'tipo_incidente': ['exact'],
            'prioridad': ['exact'],
            'impacto_incidente': ['exact'],
            'estado_incidente': ['exact'],
            'intencionalidad': ['exact'],
        }
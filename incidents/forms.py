from django import forms
from .models import Incidente
from users.models import Persona
from django.contrib.auth.models import Group


class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['titulo', 'descripcion', 'area_afectada']

class IncidenteReporteOficialForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = [
            'origen_incidente', 'recursos_afectados', 
            'contramedidas', 'otra_informacion',
            'peligrosidad', 'sistema_operativo', 'subcategoria'
        ]


class IncidenteClasificacionInternaForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = [
            'alcance', 'indicador_compromiso', 'vector_ataque',
            'fuente_deteccion', 'tecnologia', 'tipo_incidente',
            'impacto_incidente', 'intencionalidad', 'involucrados'
        ]
        widgets = {
            'involucrados': forms.CheckboxSelectMultiple(),
            'indicador_compromiso': forms.CheckboxSelectMultiple(),
        }

class IncidenteTemporalidadForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['fecha_ocurrencia', 'fecha_solucion']
        widgets = {
            'fecha_ocurrencia': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_solucion': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
from django import forms
from .models import Incidente, Evidencia_Incidente
from references.models import Subcategoria, Categoria
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrupar subcategorías por categoría
        choices = [('', '---------')]
        for categoria in Categoria.objects.all():
            subcategorias = Subcategoria.objects.filter(categoria=categoria)
            if subcategorias.exists():
                grupo = (
                    categoria.name,
                    [(s.pk, s.name) for s in subcategorias]
                )
                choices.append(grupo)
        self.fields['subcategoria'].choices = choices

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




class EvidenciaIncidenteForm(forms.ModelForm):
    class Meta:
        model = Evidencia_Incidente
        fields = ['archivo']    
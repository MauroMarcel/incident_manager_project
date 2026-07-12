from django import forms
from .models import Incidente, Evidencia_Incidente, MensajeIncidente
from references.models import Subcategoria, Categoria
from users.models import Persona
from organization.models import Area
from django.contrib.auth.models import Group


class IncidenteForm(forms.ModelForm):
    especialista_asignado = forms.ModelChoiceField(
        queryset=Persona.objects.filter(
            usuario_django__groups__name='Especialista',
            active=True
        ),
        required=True,
        label="Especialista",
        empty_label="Seleccione un especialista",
        widget=forms.Select(attrs={'class': 'sgic-form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialista_asignado'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellidos}"
    areas_afectadas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        required=True,
        label="Áreas afectadas",
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Incidente
        fields = ['titulo', 'descripcion', 'areas_afectadas', 'especialista_asignado']
    

class IncidenteReporteOficialForm(forms.ModelForm):

    class Meta:
        model = Incidente
        fields = [
            'origen_incidente', 'recursos_afectados', 
            'contramedidas', 'otra_informacion',
            'peligrosidad', 'sistema_operativo', 'subcategoria'
        ]
        labels = {
            'origen_incidente': 'Origen del incidente',
            'recursos_afectados': 'Recursos afectados',
            'contramedidas': 'Contramedidas',
            'otra_informacion': 'Otra información',
            'peligrosidad': 'Peligrosidad',
            'sistema_operativo': 'Sistema operativo',
            'subcategoria': 'Subcategoría',
        }
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
            'impacto_incidente', 'intencionalidad', 'involucrados',
            'areas_afectadas'
        ]
        labels = {
            'indicador_compromiso': 'Indicador(es) de compromiso',
            'vector_ataque': 'Vector de ataque',
            'fuente_deteccion': 'Fuente de detección',
            'tecnologia': 'Tecnología',
            'tipo_incidente': 'Tipo de incidente',
            'impacto_incidente': 'Impacto del incidente',
            'areas_afectadas': 'Áreas afectadas',
        }
        widgets = {
            'involucrados': forms.CheckboxSelectMultiple(),
            'indicador_compromiso': forms.CheckboxSelectMultiple(),
            'areas_afectadas': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['involucrados'].queryset = Persona.objects.all()

class IncidenteTemporalidadForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['fecha_ocurrencia', 'fecha_solucion']
        labels = {
            'fecha_ocurrencia': 'Fecha de inicio',
            'fecha_solucion': 'Fecha de cierre',
        }
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

    def clean(self):
        cleaned = super().clean()
        deteccion = cleaned.get('fecha_ocurrencia')
        cierre = cleaned.get('fecha_solucion')
        reporte = self.instance.fecha_reportado
        asignacion = self.instance.fecha_asignacion

        if deteccion:
            if cierre and deteccion > cierre:
                self.add_error('fecha_ocurrencia', 'La fecha de inicio no puede ser mayor que la fecha de cierre.')
            if reporte and deteccion > reporte:
                self.add_error('fecha_ocurrencia', 'La fecha de inicio no puede ser mayor que la fecha de detección.')
            if asignacion and deteccion > asignacion:
                self.add_error('fecha_ocurrencia', 'La fecha de inicio no puede ser mayor que la fecha de asignación.')

        if reporte:
            if asignacion and reporte > asignacion:
                self.add_error('fecha_ocurrencia', 'La fecha de detección no puede ser mayor que la fecha de asignación.')
            if cierre and reporte > cierre:
                self.add_error('fecha_solucion', 'La fecha de detección no puede ser mayor que la fecha de cierre.')

        if asignacion and cierre and asignacion > cierre:
            self.add_error('fecha_solucion', 'La fecha de asignación no puede ser mayor que la fecha de cierre.')

        return cleaned




class EvidenciaIncidenteForm(forms.ModelForm):
    class Meta:
        model = Evidencia_Incidente
        fields = ['archivo']

class MensajeIncidenteForm(forms.ModelForm):
    class Meta:
        model = MensajeIncidente
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'sgic-form-control',
                'rows': 2,
                'placeholder': 'Escriba un mensaje...',
                'style': 'resize:none;'
            })
        }
        labels = {
            'contenido': ''
        }
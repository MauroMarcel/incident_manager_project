from django import forms
from .models import Incidente




class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = [
            'titulo', 'descripcion',
            'fecha_deteccion', 'reportado_por', 'asignado_a',
            'entidad_afectada', 'dependencia_afectada',
            'origen_incidente', 'sistema_operativo',
            'sistemas_afectados', 'recursos_afectados',
            'acciones_tomadas', 'evidencias', 'otra_informacion'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del incidente'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del incidente'
            }),
            'fecha_deteccion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reportado_por': forms.Select(attrs={
                'class': 'form-select'
            }),
            'asignado_a': forms.Select(attrs={
                'class': 'form-select'
            }),
            'entidad_afectada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entidad u organismo afectado'
            }),
            'dependencia_afectada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dependencia afectada'
            }),
            'origen_incidente': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Origen del incidente si se conoce'
            }),
            'sistema_operativo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Windows 10, Ubuntu 22.04'
            }),
            'sistemas_afectados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sistemas afectados por el incidente'
            }),
            'recursos_afectados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Recursos afectados'
            }),
            'acciones_tomadas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Acciones tomadas para mitigar el incidente'
            }),
            'evidencias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Evidencias recopiladas'
            }),
            'otra_informacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Otra información de interés'
            }),
        }
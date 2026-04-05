from django import forms
from .models import Incidente, Tipo_Incidente


class Tipo_IncidenteForm(forms.ModelForm):
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

    class Meta:
        model = Tipo_Incidente
        fields = ['code', 'name', 'descripcion', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: MAL'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Malware'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tipo de incidente'
            }),
        }


class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = [
            'titulo', 'descripcion', 'tipo_incidente',
            'estado', 'impacto', 'fecha_deteccion',
            'reportado_por', 'asignado_a',
            'sistemas_afectados', 'acciones_tomadas', 'evidencias'
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
            'tipo_incidente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'impacto': forms.Select(attrs={
                'class': 'form-select'
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
            'sistemas_afectados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sistemas afectados por el incidente'
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
        }
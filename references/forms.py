from django import forms
from .models import Departamento, Clasificacion_Sistema, Criticidad


class DepartamentoForm(forms.ModelForm):
    """Formulario para crear/editar Departamento"""
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Departamento
        fields = ['code', 'name', 'centro_costo', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: IT',
                'maxlength': '20'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Información y Tecnología',
                'maxlength': '100'
            }),
            'centro_costo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CC-001',
                'maxlength': '50'
            }),
        }


class ClasificacionSistemaForm(forms.ModelForm):
    """Formulario para crear/editar Clasificacion_Sistema"""
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Clasificacion_Sistema
        fields = ['code', 'name', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: APP',
                'maxlength': '20'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Aplicacion',
                'maxlength': '100'
            }),
        }


class CriticidadForm(forms.ModelForm):
    """Formulario para crear/editar Criticidad"""
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Criticidad
        fields = ['code', 'name', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: A',
                'maxlength': '20'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Alta',
                'maxlength': '100'
            }),
        }

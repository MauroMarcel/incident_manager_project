from django import forms
from .models import Persona, Categoria_Persona, Cargo, Estado_Persona


class Categoria_PersonaForm(forms.ModelForm):
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Categoria_Persona
        fields = ['code', 'name', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
        }


class CargoForm(forms.ModelForm):
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Cargo
        fields = ['code', 'name', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cargo'
            }),
        }


class Estado_PersonaForm(forms.ModelForm):
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Estado_Persona
        fields = ['code', 'name', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del estado'
            }),
        }





class PersonaForm(forms.ModelForm):
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta:
        model = Persona
        fields = [
            'identificador_interno', 'nombre', 'apellidos', 'email', 'categoria_persona', 'cargo', 'estado_persona', 'jefe_directo', 'fecha_baja',
            'usuario_django', 'active'
        ]
        widgets = {
            'identificador_interno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identificador único'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'categoria_persona': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado_persona': forms.Select(attrs={
                'class': 'form-select'
            }),
            'jefe_directo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_baja': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'usuario_django': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

from django import forms
from .models import Notificacion
from django.core.validators import RegexValidator

class NotificacionForm(forms.ModelForm):
    asunto = forms.CharField(
        widget=forms.TextInput(attrs={
            'list': 'asunto-list',
            'placeholder': 'Escribe o selecciona un asunto...'
        })
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+53 5 1234567'
        }),
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{7,15}$',
                message='Introduce un número de teléfono válido.'
            )
        ]
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )

    class Meta:
        model = Notificacion
        fields = ['asunto', 'descripcion', 'telefono', 'email', 'area_notificacion']
        labels = {
            'descripcion': 'Descripci\u00f3n',
            'telefono': 'Tel\u00e9fono',
            'area_notificacion': '\u00bfD\u00f3nde est\u00e1 ocurriendo el incidente?',
        }

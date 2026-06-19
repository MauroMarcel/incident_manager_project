from django import forms
from .models import Notificacion
from django.core.validators import RegexValidator

class NotificacionForm(forms.ModelForm):
    telefono = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{7,15}$',
                message='Introduce un número de teléfono válido.'
            )
        ]
    )
    class Meta:
        model = Notificacion
        fields = ['asunto', 'descripcion', 'telefono', 'area_notificacion']
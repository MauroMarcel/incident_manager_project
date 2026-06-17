from django import forms
from .models import Notificacion

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['asunto', 'descripcion', 'telefono', 'area_notificacion']
from django import forms
from .models import IoC

class IoCForm(forms.ModelForm):
    class Meta:
        model = IoC
        fields = ['tipo_ioc', 'valor', 'descripcion']
from django import forms
from .models import Incidente
from users.models import Persona
from django.contrib.auth.models import Group

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['titulo', 'descripcion', 'area_afectada', 'especialista_asignado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        especialistas = Group.objects.get(name='Especialista')
        self.fields['especialista_asignado'].queryset = Persona.objects.filter(
            usuario_django__groups=especialistas,
            estado_persona__code='ACT'
        )
        self.fields['especialista_asignado'].label = 'Especialista a asignar'
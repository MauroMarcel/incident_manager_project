from django import forms
from django.contrib.auth.models import User, Group
from .models import Persona, Categoria_Persona, Cargo, Estado_Persona

class PersonaForm(forms.ModelForm):
    es_usuario = forms.BooleanField(required=False, label='¿Registrar como usuario del sistema?',initial=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), required=False, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), required=False, label='Confirmar contraseña')
    rol = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Rol')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Persona.objects.filter(active=True)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        self.fields['jefe_directo'].queryset = qs
        self.fields['categoria_persona'].label = 'Categoria'
        self.fields['estado_persona'].label = 'Estado'
    class Meta:
        model = Persona
        fields = [
            'identificador_interno', 'nombre', 'apellidos', 
            'email', 'area', 'cargo', 'categoria_persona',
            'estado_persona', 'jefe_directo'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        es_usuario = cleaned_data.get('es_usuario')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        rol = cleaned_data.get('rol')
        
        if es_usuario:
            if not password1:
                self.add_error('password1', 'La contraseña es obligatoria.')
            if password1 != password2:
                self.add_error('password2', 'Las contraseñas no coinciden.')
            if not rol:
                self.add_error('rol', 'Debe asignar un rol al usuario.')
        
        return cleaned_data

class PersonaUpdateForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nombre', 'apellidos', 'email', 'area',
            'cargo', 'categoria_persona', 'estado_persona',
            'jefe_directo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Persona.objects.filter(active=True)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        self.fields['jefe_directo'].queryset = qs
        self.fields['area'].required = True
        self.fields['categoria_persona'].label = 'Categoria'
        self.fields['estado_persona'].label = 'Estado'


class Categoria_PersonaForm(forms.ModelForm):
    class Meta:
        model = Categoria_Persona
        fields = ['code', 'name', 'active']


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['code', 'name', 'active']


class Estado_PersonaForm(forms.ModelForm):
    class Meta:
        model = Estado_Persona
        fields = ['code', 'name', 'active']
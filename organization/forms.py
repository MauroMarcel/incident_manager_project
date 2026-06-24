from django import forms
from .models import Area

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'area_superior']
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        area_superior = cleaned_data.get('area_superior')
        
        if Area.objects.filter(
            nombre=nombre,
            area_superior=area_superior
        ).exists():
            raise forms.ValidationError(
                'Ya existe un área con ese nombre bajo la misma área superior.'
            )
        return cleaned_data
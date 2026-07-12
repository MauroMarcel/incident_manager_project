from django import forms
from .models import Area

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'area_superior']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            exclude_ids = self._get_descendant_ids(self.instance)
            self.fields['area_superior'].queryset = Area.objects.exclude(
                pk__in=exclude_ids
            )

    def _get_descendant_ids(self, area):
        ids = [area.pk]
        for sub in area.subareas.all():
            ids.extend(self._get_descendant_ids(sub))
        return ids

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        area_superior = cleaned_data.get('area_superior')

        if self.instance and self.instance.pk and area_superior:
            if area_superior.pk in self._get_descendant_ids(self.instance):
                raise forms.ValidationError(
                    'El área superior seleccionada crea una referencia circular.'
                )

        qs = Area.objects.filter(nombre=nombre, area_superior=area_superior)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                'Ya existe un área con ese nombre bajo la misma área superior.'
            )
        return cleaned_data
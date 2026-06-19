from django.contrib import admin
from .models import Incidente


class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'fecha_reportado')
    filter_horizontal = ('involucrados', 'indicador_compromiso')
    search_fields = ('codigo', 'titulo', 'descripcion')


admin.site.register(Incidente, IncidenteAdmin)

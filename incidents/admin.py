from django.contrib import admin
from .models import Incidente, Evidencia_Incidente


class EvidenciaIncidenteInline(admin.TabularInline):
    model = Evidencia_Incidente
    extra = 0

class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'fecha_reportado')
    filter_horizontal = ('involucrados', 'indicador_compromiso')
    inlines = [EvidenciaIncidenteInline]
    search_fields = ('codigo', 'titulo', 'descripcion')


admin.site.register(Incidente, IncidenteAdmin)
admin.site.register(Evidencia_Incidente)

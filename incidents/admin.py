from django.contrib import admin
from .models import Incidente, Evidencia_Incidente, MensajeIncidente


class EvidenciaIncidenteInline(admin.TabularInline):
    model = Evidencia_Incidente
    extra = 0

class MensajeIncidenteInline(admin.TabularInline):
    model = MensajeIncidente
    extra = 0
    readonly_fields = ('remitente', 'fecha_creacion')
    ordering = ('-fecha_creacion',)

class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'fecha_reportado')
    filter_horizontal = ('involucrados', 'indicador_compromiso')
    inlines = [EvidenciaIncidenteInline, MensajeIncidenteInline]
    search_fields = ('codigo', 'titulo', 'descripcion')


admin.site.register(Incidente, IncidenteAdmin)
admin.site.register(Evidencia_Incidente)
admin.site.register(MensajeIncidente)

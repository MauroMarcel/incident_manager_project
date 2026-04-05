from django.contrib import admin
from .models import Incidente, Tipo_Incidente

@admin.register(Tipo_Incidente)
class Tipo_IncidenteAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'active']
    search_fields = ['code', 'name']

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', 'estado', 'impacto', 'tipo_incidente', 'reportado_por', 'fecha_reporte']
    search_fields = ['codigo', 'titulo']
    list_filter = ['estado', 'impacto', 'tipo_incidente']
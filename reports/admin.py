from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_reporte', 'generado_por', 'created']
    list_filter = ['tipo_reporte', 'created']

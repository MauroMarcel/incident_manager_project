from django.contrib import admin
from .models import Incidente

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'fecha_reportado')
    list_filter = ()
    search_fields = ('codigo', 'titulo', 'descripcion')

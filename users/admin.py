from django.contrib import admin
from .models import Persona, ConfiguracionAltaGerencia


class PersonaAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('identificador_interno', 'nombre', 'apellidos', 'email', 'cargo', 'estado_persona')
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('nombre',)
    #para colocar una barra de busqueda
    search_fields = ('identificador_interno', 'nombre', 'apellidos', 'email', 'cargo', 'estado_persona')

class ConfiguracionAltaGerenciaAdmin(admin.ModelAdmin):
    filter_horizontal = ('areas_supervision',)



admin.site.register(Persona, PersonaAdmin)
admin.site.register(ConfiguracionAltaGerencia, ConfiguracionAltaGerenciaAdmin)




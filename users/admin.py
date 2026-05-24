from django.contrib import admin
from .models import Persona, Categoria_Persona, Cargo, Estado_Persona
from references.admin import NomencladorAdmin


class PersonaAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('identificador_interno', 'nombre', 'apellidos', 'email', 'cargo', 'estado_persona')
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('nombre',)
    #para colocar una barra de busqueda
    search_fields = ('identificador_interno', 'nombre', 'apellidos', 'email', 'cargo', 'estado_persona')

admin.site.register(Categoria_Persona, NomencladorAdmin)
admin.site.register(Cargo, NomencladorAdmin)
admin.site.register(Estado_Persona, NomencladorAdmin)

admin.site.register(Persona, PersonaAdmin)

# Register your models here.

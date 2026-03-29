from django.contrib import admin
from .models import Departamento, Clasificacion_Sistema, Criticidad


class NomencladorAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('code', 'name',)
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('name',)


class DepartamentoAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('code', 'name', 'centro_costo')
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('name',)
    #para colocar una barra de busqueda
    search_fields = ("name", "code", "centro_costo",)
    #para añadir filtros
    list_filter = ("centro_costo","code")
    #para mostrar x cantidad de elementos por pagina (paginar)
    list_per_page = 2









admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Clasificacion_Sistema, NomencladorAdmin)
admin.site.register(Criticidad, NomencladorAdmin)

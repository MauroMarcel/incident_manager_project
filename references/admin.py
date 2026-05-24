from django.contrib import admin
# from .models import  Clasificacion_Sistema, Criticidad


class NomencladorAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('code', 'name',)
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('name',)








# admin.site.register(Departamento, DepartamentoAdmin)
# admin.site.register(Clasificacion_Sistema, NomencladorAdmin)
#admin.site.register(Criticidad, NomencladorAdmin)

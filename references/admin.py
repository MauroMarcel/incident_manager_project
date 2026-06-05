from django.contrib import admin

# Referencias — Incidentes
from references.models import (
    Categoria, Subcategoria, Prioridad, Estado_Incidente,
    Impacto_Incidente, Tipo_Incidente, Alcance, Vector_Ataque,
    Fuente_Deteccion, Tecnologia, Intencionalidad,
    Peligrosidad, Sistema_Operativo
)
# Referencias — Usuarios
from references.models import Categoria_Persona, Cargo, Estado_Persona

# Referencias — Notificaciones
from references.models import Asunto_Notificacion, Estado_Notificacion

# Referencias — IOC
from references.models import Tipo_IOC

class NomencladorAdmin(admin.ModelAdmin):
    #para mostrar una barra superior con categorias
    list_display = ('code', 'name',)
    #para colocar los links en el nombre en vez del codigo
    list_display_links = ('name',)


class SubcategoriaAdmin(NomencladorAdmin):
    list_display = ('code', 'name', 'categoria')



# ============================================================
# INCIDENTES
# ============================================================
admin.site.register(Categoria, NomencladorAdmin)
admin.site.register(Subcategoria, SubcategoriaAdmin)
admin.site.register(Prioridad, NomencladorAdmin)
admin.site.register(Estado_Incidente, NomencladorAdmin)
admin.site.register(Impacto_Incidente, NomencladorAdmin)
admin.site.register(Tipo_Incidente, NomencladorAdmin)
admin.site.register(Alcance, NomencladorAdmin)
admin.site.register(Vector_Ataque, NomencladorAdmin)
admin.site.register(Fuente_Deteccion, NomencladorAdmin)
admin.site.register(Tecnologia, NomencladorAdmin)
admin.site.register(Intencionalidad, NomencladorAdmin)
admin.site.register(Peligrosidad, NomencladorAdmin)
admin.site.register(Sistema_Operativo, NomencladorAdmin)
# ============================================================
# USUARIOS
# ============================================================
admin.site.register(Categoria_Persona, NomencladorAdmin)
admin.site.register(Cargo, NomencladorAdmin)
admin.site.register(Estado_Persona, NomencladorAdmin)
# ============================================================
# NOTIFICACIONES
# ============================================================
admin.site.register(Asunto_Notificacion, NomencladorAdmin)
admin.site.register(Estado_Notificacion, NomencladorAdmin)
# ============================================================
# INDICADORES DE COMPROMISO
# ============================================================
admin.site.register(Tipo_IOC, NomencladorAdmin)

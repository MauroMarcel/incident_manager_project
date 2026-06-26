from django.contrib import admin
from .models import Notificacion, Evidencia_Notificacion


class EvidenciaNotificacionInline(admin.TabularInline):
    model = Evidencia_Notificacion
    extra = 0
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_notificador', 'asunto', 'fecha_notificacion', 'estado_notificacion')
    search_fields = ('usuario_notificador__username', 'asunto__nombre', 'descripcion')
    list_filter = ('estado_notificacion', 'fecha_notificacion', 'usuario_notificador')
    inlines = [EvidenciaNotificacionInline]



admin.site.register(Notificacion, NotificacionAdmin)
admin.site.register(Evidencia_Notificacion)


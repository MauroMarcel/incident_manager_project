from django.contrib import admin
from .models import Notificacion, Evidencia_Notificacion

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_notificador', 'asunto', 'fecha_notificacion', 'estado_notificacion')
    search_fields = ('usuario_notificador__username', 'asunto__nombre', 'descripcion')
    list_filter = ('estado_notificacion', 'fecha_notificacion', 'usuario_notificador')



admin.site.register(Notificacion, NotificacionAdmin)


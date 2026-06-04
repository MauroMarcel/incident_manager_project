from django.db import models
from django.conf import settings
from base.models import ModeloBase 
from references.models import Asunto_Notificacion, Estado_Notificacion
from organization.models import Area
from incidents.models import Incidente

class Notificacion(ModeloBase):
    usuario_notificador =models.ForeignKey(
        settings.AUTH_USER_MODEL
        , on_delete=models.PROTECT,
        related_name='usuarios_notificadores'
    )
    asunto = models.ForeignKey(
        Asunto_Notificacion,
        on_delete=models.PROTECT, 
        related_name='asuntos'
        )
    descripcion = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True, null=False)

    
    telefono = models.CharField(max_length=20, blank=True, null=True)
    area_notificacion = models.ForeignKey(
        Area,
        on_delete=models.PROTECT, 
        related_name='areas_notificacion',
        blank=True,
        null=True
        )
    
    respuesta_supervisor = models.TextField(blank=True, null=True)
    estado_notificacion = models.ForeignKey(
        Estado_Notificacion,
        on_delete=models.PROTECT, 
        related_name='estados_notificacion'
        )
    incidente_asociado=models.ForeignKey(
        Incidente,
        on_delete=models.SET_NULL, 
        related_name='notificaciones_incidente',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['created']



class Evidencia_Notificacion(ModeloBase):
    notificacion = models.ForeignKey(
        Notificacion,
        on_delete=models.CASCADE, 
        related_name='evidencias',
        null=True,
        blank=True
        )
    archivo = models.FileField(upload_to='evidencias_notificaciones/')

    class Meta:
        verbose_name = "Evidencia de la Notificación"
        verbose_name_plural = "Evidencias de la Notificación"
        ordering = ['created']
from django.db import models
from references.models import Tipo_IOC
from base.models import ModeloBase

class IoC(ModeloBase):
    tipo_ioc = models.ForeignKey(
        Tipo_IOC,
        on_delete=models.PROTECT, 
        related_name='iocs'
        )
    valor = models.CharField(max_length=255)
    descripcion=models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "Indicador de Compromiso (IOC)"
        verbose_name_plural = "Indicadores de Compromiso (IOCs)"
    
    def __str__(self):
        return f"{self.tipo_ioc} — {self.valor}"
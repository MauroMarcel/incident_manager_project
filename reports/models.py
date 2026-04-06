from django.db import models
from references.models import ModeloBase
from incidents.models import Incidente
from users.models import Persona


class Reporte(ModeloBase):

    TIPO_REPORTE = (
        ('GEN', 'Reporte General'),
        ('EST', 'Reporte por Estado'),
        ('IMP', 'Reporte por Impacto'),
        ('TIP', 'Reporte por Tipo'),
    )

    titulo = models.CharField(max_length=200)
    tipo_reporte = models.CharField(max_length=3, choices=TIPO_REPORTE)
    descripcion = models.TextField(blank=True)
    generado_por = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ['-created']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_reporte_display()})"
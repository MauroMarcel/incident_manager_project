from django.db import models
from references.models import ModeloBase, Modelo_Nomenclador
from users.models import Persona
import datetime


# ============================================================
# NOMENCLADOR
# ============================================================

class Tipo_Incidente(Modelo_Nomenclador):
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Incidente"
        verbose_name_plural = "Tipos de Incidentes"
        ordering = ['name']


# ============================================================
# INCIDENTE
# ============================================================

class Incidente(ModeloBase):

    ESTADOS = (
        ('REP', 'Reportado'),
        ('ASI', 'Asignado'),
        ('INV', 'En Investigación'),
        ('CON', 'Contenido'),
        ('ERD', 'Eradicado'),
        ('RCV', 'Recuperación'),
        ('RES', 'Resuelto'),
        ('CER', 'Cerrado'),
        ('RCH', 'Rechazado'),
    )

    IMPACTO = (
        ('B', 'Bajo'),
        ('M', 'Medio'),
        ('A', 'Alto'),
        ('X', 'Extremo'),
    )

    VIA_REPORTE = (
        ('TEL', 'Teléfono'),
        ('EMA', 'Correo Electrónico'),
        ('PRE', 'Presencial'),
        ('SIS', 'Sistema Automatizado'),
        ('OTR', 'Otro'),
    )

    # Identificación
    codigo = models.CharField(max_length=20, unique=True, editable=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    # Clasificación
    tipo_incidente = models.ForeignKey(
        Tipo_Incidente,
        on_delete=models.SET_NULL,
        null=True
    )
    estado = models.CharField(max_length=3, choices=ESTADOS, default='REP')
    impacto = models.CharField(max_length=1, choices=IMPACTO, default='M')

    # Fechas
    fecha_deteccion = models.DateTimeField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    # Datos del informante
    via_reporte = models.CharField(
        max_length=3, choices=VIA_REPORTE, default='EMA'
    )

    # Personas involucradas
    reportado_por = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incidentes_reportados'
    )
    asignado_a = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes_asignados'
    )

    # Datos de la entidad afectada
    entidad_afectada = models.CharField(max_length=200, blank=True)
    dependencia_afectada = models.CharField(max_length=200, blank=True)

    # Detalles técnicos
    origen_incidente = models.TextField(blank=True)
    sistema_operativo = models.CharField(max_length=100, blank=True)
    sistemas_afectados = models.TextField(blank=True)
    recursos_afectados = models.TextField(blank=True)
    acciones_tomadas = models.TextField(blank=True)
    evidencias = models.TextField(blank=True)
    otra_informacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"
        ordering = ['-fecha_reporte']

    def save(self, *args, **kwargs):
        if not self.codigo:
            year = datetime.datetime.now().year
            ultimo = Incidente.objects.filter(
                codigo__startswith=f'INC-{year}-'
            ).count()
            self.codigo = f'INC-{year}-{str(ultimo + 1).zfill(3)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"
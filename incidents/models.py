from django.db import models
from base.models import ModeloBase
from references.models import Tipo_Incidente, Estado_Incidente, Impacto_Incidente, Alcance, Vector_Ataque, Sistema_Operativo, Fuente_Deteccion, Tecnologia, Intencionalidad, Peligrosidad, Subcategoria, Prioridad
from users.models import Persona
from IoC.models import IoC
from organization.models import Area 
import datetime


class Incidente(ModeloBase):

# ============================================================
# NÚCLEO
# ============================================================
    codigo = models.CharField(max_length=20, unique=True, editable=False, null=False, blank=False)
    titulo = models.CharField(max_length=200, null=False, blank=False)
    descripcion = models.TextField(blank=False)
    areas_afectadas = models.ManyToManyField(
        Area,
        related_name='incidentes_area',
        blank=True
    )
# ============================================================
# REPORTE OFICIAL — RESOLUCIÓN 105/2025
# ============================================================
    origen_incidente = models.TextField(blank=True)

    recursos_afectados = models.TextField(blank=True)
    contramedidas = models.TextField(blank=True)
    otra_informacion = models.TextField(blank=True)
    peligrosidad = models.ForeignKey(
        Peligrosidad,
        on_delete=models.PROTECT, 
        related_name="niveles_peligrosidad_incidente",
        null=True,
        blank=True
        )
    sistema_operativo = models.ForeignKey(
        Sistema_Operativo,
        on_delete=models.PROTECT,
        related_name='sistemas_operativos_afectados_incidente',
        null=True,
        blank=True
    )
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.PROTECT,
        related_name='subcategorias_incidente',
        null=True,
        blank=True
    )
# ============================================================
# CLASIFICACIÓN INTERNA
# ============================================================
    alcance = models.ForeignKey(
        Alcance,
        on_delete=models.PROTECT,   
        related_name='alcance_incidente',
        null=True,
        blank=True
    )
    indicador_compromiso=models.ManyToManyField(
        IoC,
        related_name='indicadores_compromiso_incidente',
        blank=True
    )
    
    vector_ataque = models.ForeignKey(
        Vector_Ataque,
        on_delete=models.PROTECT,
        related_name='vectores_ataque_incidente',
        null=True,
        blank=True
    )
    fuente_deteccion = models.ForeignKey(
        Fuente_Deteccion,
        on_delete=models.PROTECT,
        related_name='fuentes_deteccion_incidente',
        null=True,
        blank=True
    )
    tecnologia = models.ForeignKey(
        Tecnologia,
        on_delete=models.PROTECT,
        related_name='tecnologias_afectadas_incidente',
        null=True,
        blank=True
    )
    tipo_incidente = models.ForeignKey(
        Tipo_Incidente,
        on_delete=models.PROTECT,
        related_name='tipos_incidente',
        null=True,
        blank=True
    )
    prioridad = models.ForeignKey(
        Prioridad,
        on_delete=models.PROTECT,
        related_name='niveles_prioridad_incidente',
        null=True,
        blank=True
    )
    impacto_incidente = models.ForeignKey(
        Impacto_Incidente,
        on_delete=models.PROTECT,
        related_name='impactos_incidente',
        null=True,
        blank=True
    )
    estado_incidente = models.ForeignKey(
        Estado_Incidente,
        on_delete=models.PROTECT,
        related_name='estados_incidente',
        null= True,
        blank=True
    )
    intencionalidad = models.ForeignKey(
        Intencionalidad,
        on_delete=models.PROTECT,
        related_name='intencionalidades_incidente',
        null=True,
        blank=True
    )
# ============================================================
# PERSONAS IMPLICADOS
# ============================================================
    supervisor = models.ForeignKey(
        Persona,
        on_delete=models.PROTECT,
        related_name='supervisores_incidente',
        null=False, 
        blank=False
    )
    especialista_asignado = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        related_name='especialistas_incidente',
        null=True,
        blank=True
    )
    involucrados = models.ManyToManyField(
        Persona,
        related_name='personas_involucradas_incidente',
        blank=True
    )
# ============================================================
# TEMPORALIDAD
# ============================================================
    fecha_ocurrencia = models.DateTimeField(null=True, blank=True)
    fecha_reportado = models.DateTimeField(null=False,blank=False)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_solucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"
        ordering = ['fecha_reportado']

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



class MensajeIncidente(models.Model):
    incidente = models.ForeignKey(
        Incidente,
        on_delete=models.CASCADE,
        related_name='mensajes'
    )
    remitente = models.ForeignKey(
        Persona,
        on_delete=models.PROTECT,
        related_name='mensajes_incidente'
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensaje del incidente"
        verbose_name_plural = "Mensajes del incidente"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"[{self.incidente.codigo}] {self.remitente} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"


class Evidencia_Incidente(ModeloBase):
    incidente = models.ForeignKey(
        Incidente,
        on_delete=models.CASCADE,
        related_name='evidencias',
    )
    archivo = models.FileField(upload_to='evidencias_incidentes/')
    class Meta:
        verbose_name = "Evidencia del Incidente"
        verbose_name_plural = "Evidencias del Incidente"
        ordering = ['created']


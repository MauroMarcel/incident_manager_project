from django.db import models
from base.models import ModeloBase, Modelo_Nomenclador

# ============================================================
# NOMENCLADORES DE INCIDENTES
# ============================================================

class Categoria(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

class Subcategoria(Modelo_Nomenclador):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT, 
        related_name='subcategorias'
        )
    class Meta:
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"
        ordering = ['name']

class Prioridad(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"
        ordering = ['name']

class Estado_Incidente(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Estado del Incidente"
        verbose_name_plural = "Estados del Incidente"
        ordering = ['name']

class Impacto_Incidente(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Impacto del Incidente"
        verbose_name_plural = "Impactos del Incidente"
        ordering = ['name']

class Tipo_Incidente(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Tipo del Incidente"
        verbose_name_plural = "Tipos del Incidente"
        ordering = ['name']

class Alcance(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Alcance del Incidente"
        verbose_name_plural = "Alcances del Incidente"
        ordering = ['name']

class Vector_Ataque(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Vector de Ataque"
        verbose_name_plural = "Vectores de Ataque"
        ordering = ['name']

class Fuente_Deteccion(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Fuente de Detección"
        verbose_name_plural = "Fuentes de Detección"
        ordering = ['name']

class Tecnologia(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Tecnología"
        verbose_name_plural = "Tecnologías"
        ordering = ['name']

class Intencionalidad(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Intencionalidad del Ataque"
        verbose_name_plural = "Intencionalidades del Ataque"
        ordering = ['name']

class Peligrosidad(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Peligrosidad del Incidente"
        verbose_name_plural = "Peligrosidades del Incidente"
        ordering = ['name']

class Sistema_Operativo(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Sistema Operativo"
        verbose_name_plural = "Sistemas Operativos"
        ordering = ['name']

# ============================================================
# NOMENCLADORES DE USUARIOS
# ============================================================

class Categoria_Persona(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Categoria_Persona"
        verbose_name_plural = "Categorias de Persona"
        ordering = ['name']

class Cargo(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['name']

class Estado_Persona(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Estado_Persona"
        verbose_name_plural = "Estados de Persona"
        ordering = ['name']

# ============================================================
# NOMENCLADORES DE NOTIFICACIONES
# ============================================================
class Asunto_Notificacion(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Asunto de Notificación"
        verbose_name_plural = "Asuntos de Notificación"
        ordering = ['name']

class Estado_Notificacion(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Estado de Notificación"
        verbose_name_plural = "Estados de Notificación"
        ordering = ['name']

# ============================================================
# NOMENCLADORES DE INDICADORES DE COMPROMISO (IOC)
# ============================================================

class Tipo_IOC(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Tipo de IOC"
        verbose_name_plural = "Tipos de IOC"
        ordering = ['name']


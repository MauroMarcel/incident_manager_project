from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import uuid
# Create your models here.
class ModeloBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
class Modelo_Nomenclador(ModeloBase):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        abstract = True
        ordering = ['name']
    
    def __str__(self):
        return f"({self.code}) {self.name}"
    

class Departamento(Modelo_Nomenclador):
    centro_costo = models.CharField(max_length=50, blank=True)
    #jefe_departamento = models.ForeignKey('Persona',on_delete=models.SET_NULL,null=True,blank=True,related_name='departamentos_dirigidos')
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['name']
    


class Clasificacion_Sistema(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Clasificacion_Sistema"
        verbose_name_plural = "Clasificacion_Sistemas"
        ordering = ['name']
        

class Criticidad(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Criticidad"
        verbose_name_plural = "Criticidades"
        ordering = ['name']
        
    


'''
('DIR', 'Directorio Activo'),

('APP', 'Aplicación'),

('DB', 'Base de Datos'),

        ('SRV', 'Servidor'),

        ('SaaS', 'Software como Servicio'),

        ('NET', 'Red/Infraestructura'),

    )

    CRITICIDAD = (

        ('B', 'Baja'),

        ('M', 'Media'),

        ('A', 'Alta'),

        ('C', 'Crítica'),

    )

    nombre = models.CharField(max_length=200)

    codigo = models.CharField(max_length=50, unique=True)

    tipo = models.CharField(max_length=20, choices=TIPO_SISTEMA)

    criticidad = models.CharField(max_length=1, choices=CRITICIDAD, default='M')

    descripcion = models.TextField(blank=True)

    responsable = models.ForeignKey(

        'Persona',

        on_delete=models.SET_NULL,

        null=True,

        related_name='sistemas_responsable'

    )

    url_acceso = models.URLField(blank=True)

    class Meta:

        verbose_name = "Sistema"

        verbose_name_plural = "Sistemas"

        ordering = ['nombre']

    def __str__(self):

        return f"{self.codigo} - {self.nombre}"
'''
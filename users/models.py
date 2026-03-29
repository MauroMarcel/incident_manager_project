from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from references.models import Departamento, ModeloBase, Modelo_Nomenclador
import uuid


class Categoria_Persona(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Categoria_Persona"
        verbose_name_plural = "Categorias_Personas"
        ordering = ['name']

class Cargo(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['name']

class Estado_Persona(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Estado_Persona"
        verbose_name_plural = "Estados_Personas"
        ordering = ['name']

class Nivel_Privilegio(Modelo_Nomenclador):
    class Meta:
        verbose_name = "Nivel_Privilegio"
        verbose_name_plural = "Niveles_Privilegios"
        ordering = ['name']


class Persona(ModeloBase):
    identificador_interno = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    departamento = models.ForeignKey(Departamento,on_delete=models.SET_NULL,null=True,)
    categoria_persona = models.ForeignKey(Categoria_Persona,on_delete=models.SET_NULL,null=True,)
    cargo = models.ForeignKey(Cargo,on_delete=models.SET_NULL,null=True,)
    estado_persona = models.ForeignKey(Estado_Persona,on_delete=models.SET_NULL,null=True,)
    nivel_privilegio = models.ForeignKey(Nivel_Privilegio,on_delete=models.SET_NULL,null=True,)
    jefe_directo = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='subordinados')
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    usuario_django = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='perfil_persona')
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['apellidos', 'nombre'] #indexes = [models.Index(fields=['jefe_directo']),models.Index(fields=['departamento', 'estado']),]
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.identificador_interno})"


from django.conf import settings
from django.db import models
from references.models import ModeloBase
from references.models import Categoria_Persona, Cargo, Estado_Persona


class Persona(ModeloBase):
    identificador_interno = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    categoria_persona = models.ForeignKey(Categoria_Persona,on_delete=models.SET_NULL,null=True,)
    cargo = models.ForeignKey(Cargo,on_delete=models.SET_NULL,null=True,)
    estado_persona = models.ForeignKey(Estado_Persona,on_delete=models.SET_NULL,null=True,)
    jefe_directo = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='subordinados')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateField(null=True, blank=True)
    usuario_django = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='perfil_persona')
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['apellidos', 'nombre'] 
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.identificador_interno})"


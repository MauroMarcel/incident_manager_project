from django.conf import settings
from django.db import models
from organization.models import Area
from references.models import ModeloBase
from references.models import Categoria_Persona, Cargo, Estado_Persona


class Persona(ModeloBase):
    identificador_interno = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    categoria_persona = models.ForeignKey(Categoria_Persona,on_delete=models.SET_NULL,null=True,)
    cargo = models.ForeignKey(Cargo,on_delete=models.SET_NULL,null=True,)
    estado_persona = models.ForeignKey(Estado_Persona,on_delete=models.SET_NULL,null=True,)
    jefe_directo = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='subordinados')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateField(null=True, blank=True)
    usuario_django = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfil_persona'
    )
    area = models.ForeignKey(
    Area,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='personas'
)
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['apellidos', 'nombre'] 
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.identificador_interno})"




class ConfiguracionAltaGerencia(ModeloBase):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='config_gerencia'
    )
    areas_supervision = models.ManyToManyField(
        Area,
        blank=True,
        related_name='supervisores_gerencia'
    )

    class Meta:
        verbose_name = "Configuración Alta Gerencia"
        verbose_name_plural = "Configuraciones Alta Gerencia"

    def __str__(self):
        return f"Config. gerencia — {self.persona}"

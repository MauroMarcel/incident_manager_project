import uuid
from django.db import models

# Create your models here.
class ModeloBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class Modelo_Nomenclador(ModeloBase):
    code = models.CharField(max_length=20, blank=False, unique=True)
    name = models.CharField(max_length=300, blank=False, unique=True)
    
    class Meta:
        abstract = True
        ordering = ['name']
    
    def __str__(self):
        return f"({self.code}) {self.name}"
    

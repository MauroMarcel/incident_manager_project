from django.db import models


# Create your models here.

class Area(models.Model):
    nombre = models.CharField(max_length=100)

    area_superior = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subareas'
    )
    def __str__(self):
        return self.nombre
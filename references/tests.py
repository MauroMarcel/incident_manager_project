from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# from .models import Departamento, Clasificacion_Sistema, Criticidad
import uuid




class ModeloBaseTests(TestCase):
    """Pruebas para la herencia y funcionalidad base"""
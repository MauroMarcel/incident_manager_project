from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Departamento, Clasificacion_Sistema, Criticidad
import uuid


class DepartamentoTests(TestCase):
    """Pruebas unitarias para el modelo Departamento"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.departamento = Departamento.objects.create(
            code='IT',
            name='Información y Tecnología',
            centro_costo='CC-001'
        )
    
    def test_crear_departamento(self):
        """Verifica que se crea correctamente un Departamento"""
        self.assertEqual(self.departamento.code, 'IT')
        self.assertEqual(self.departamento.name, 'Información y Tecnología')
        self.assertEqual(self.departamento.centro_costo, 'CC-001')
    
    def test_departamento_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Departamento.objects.create(
                code='IT',  # Código duplicado
                name='Otro Departamento'
            )
    
    def test_departamento_active_default(self):
        """Verifica que por defecto active es True"""
        self.assertTrue(self.departamento.active)
    
    def test_departamento_str(self):
        """Verifica la representación en string del modelo"""
        expected_str = "(IT) Información y Tecnología"
        self.assertEqual(str(self.departamento), expected_str)
    
    def test_departamento_created_timestamp(self):
        """Verifica que created se asigna automáticamente"""
        self.assertIsNotNone(self.departamento.created)
    
    def test_departamento_updated_timestamp(self):
        """Verifica que updated se asigna automáticamente"""
        self.assertIsNotNone(self.departamento.updated)
    
    def test_departamento_uuid_primary_key(self):
        """Verifica que el id es un UUID válido"""
        self.assertIsInstance(self.departamento.id, uuid.UUID)
    
    def test_departamento_centro_costo_opcional(self):
        """Verifica que centro_costo puede estar vacío"""
        dept = Departamento.objects.create(
            code='ADMIN',
            name='Administración'
        )
        self.assertEqual(dept.centro_costo, '')
    
    def test_departamento_ordenamiento(self):
        """Verifica que los departamentos se ordenan por name"""
        Departamento.objects.create(code='ZZ', name='Zona')
        Departamento.objects.create(code='AA', name='Analítica')
        
        depts = list(Departamento.objects.all())
        self.assertEqual(depts[0].name, 'Analítica')
        self.assertEqual(depts[1].name, 'Información y Tecnología')
        self.assertEqual(depts[2].name, 'Zona')
    
    def test_departamento_actualizar(self):
        """Verifica que se puede actualizar un Departamento"""
        self.departamento.name = 'TI Actualizado'
        self.departamento.save()
        
        dept_actualizado = Departamento.objects.get(id=self.departamento.id)
        self.assertEqual(dept_actualizado.name, 'TI Actualizado')
    
    def test_departamento_eliminar(self):
        """Verifica que se puede eliminar un Departamento"""
        dept_id = self.departamento.id
        self.departamento.delete()
        
        with self.assertRaises(Departamento.DoesNotExist):
            Departamento.objects.get(id=dept_id)


class ClasificacionSistemaTests(TestCase):
    """Pruebas unitarias para el modelo Clasificacion_Sistema"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.clasificacion = Clasificacion_Sistema.objects.create(
            code='SYS',
            name='Sistema'
        )
    
    def test_crear_clasificacion(self):
        """Verifica que se crea correctamente una Clasificacion_Sistema"""
        self.assertEqual(self.clasificacion.code, 'SYS')
        self.assertEqual(self.clasificacion.name, 'Sistema')
    
    def test_clasificacion_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Clasificacion_Sistema.objects.create(
                code='SYS',  # Código duplicado
                name='Otra Clasificación'
            )
    
    def test_clasificacion_active_default(self):
        """Verifica que por defecto active es True"""
        self.assertTrue(self.clasificacion.active)
    
    def test_clasificacion_str(self):
        """Verifica la representación en string"""
        expected_str = "(SYS) Sistema"
        self.assertEqual(str(self.clasificacion), expected_str)
    
    def test_clasificacion_timestamps(self):
        """Verifica que created y updated se asignan automáticamente"""
        self.assertIsNotNone(self.clasificacion.created)
        self.assertIsNotNone(self.clasificacion.updated)
    
    def test_clasificacion_uuid_primary_key(self):
        """Verifica que el id es un UUID válido"""
        self.assertIsInstance(self.clasificacion.id, uuid.UUID)
    
    def test_clasificacion_ordenamiento(self):
        """Verifica que se ordenan por name"""
        Clasificacion_Sistema.objects.create(code='APP', name='Aplicación')
        Clasificacion_Sistema.objects.create(code='DB', name='Base de Datos')
        
        clasificaciones = list(Clasificacion_Sistema.objects.all())
        self.assertEqual(clasificaciones[0].name, 'Aplicación')
        self.assertEqual(clasificaciones[1].name, 'Base de Datos')
        self.assertEqual(clasificaciones[2].name, 'Sistema')
    
    def test_clasificacion_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Clasificacion_Sistema._meta
        self.assertEqual(meta.verbose_name, 'Clasificacion_Sistema')
        self.assertEqual(meta.verbose_name_plural, 'Clasificacion_Sistemas')


class CriticidadTests(TestCase):
    """Pruebas unitarias para el modelo Criticidad"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.criticidad = Criticidad.objects.create(
            code='A',
            name='Alta'
        )
    
    def test_crear_criticidad(self):
        """Verifica que se crea correctamente una Criticidad"""
        self.assertEqual(self.criticidad.code, 'A')
        self.assertEqual(self.criticidad.name, 'Alta')
    
    def test_criticidad_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Criticidad.objects.create(
                code='A',  # Código duplicado
                name='Otra Criticidad'
            )
    
    def test_criticidad_active_default(self):
        """Verifica que por defecto active es True"""
        self.assertTrue(self.criticidad.active)
    
    def test_criticidad_str(self):
        """Verifica la representación en string"""
        expected_str = "(A) Alta"
        self.assertEqual(str(self.criticidad), expected_str)
    
    def test_criticidad_timestamps(self):
        """Verifica que created y updated se asignan automáticamente"""
        self.assertIsNotNone(self.criticidad.created)
        self.assertIsNotNone(self.criticidad.updated)
    
    def test_criticidad_uuid_primary_key(self):
        """Verifica que el id es un UUID válido"""
        self.assertIsInstance(self.criticidad.id, uuid.UUID)
    
    def test_criticidad_ordenamiento(self):
        """Verifica que se ordenan por name"""
        Criticidad.objects.create(code='B', name='Baja')
        Criticidad.objects.create(code='M', name='Media')
        
        criticidades = list(Criticidad.objects.all())
        self.assertEqual(criticidades[0].name, 'Alta')
        self.assertEqual(criticidades[1].name, 'Baja')
        self.assertEqual(criticidades[2].name, 'Media')
    
    def test_criticidad_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Criticidad._meta
        self.assertEqual(meta.verbose_name, 'Criticidad')
        self.assertEqual(meta.verbose_name_plural, 'Criticidades')


class ModeloBaseTests(TestCase):
    """Pruebas para la herencia y funcionalidad base"""
    
    def test_departamento_hereda_de_modelo_base(self):
        """Verifica que Departamento hereda campos de ModeloBase"""
        dept = Departamento.objects.create(code='TEST', name='Test')
        
        # Verifica que tiene los campos de ModeloBase
        self.assertIsNotNone(dept.id)
        self.assertIsNotNone(dept.created)
        self.assertIsNotNone(dept.updated)
        self.assertTrue(dept.active)
    
    def test_criticidad_hereda_de_modelo_base(self):
        """Verifica que Criticidad hereda campos de ModeloBase"""
        crit = Criticidad.objects.create(code='C', name='Crítica')
        
        # Verifica que tiene los campos de ModeloBase
        self.assertIsNotNone(crit.id)
        self.assertIsNotNone(crit.created)
        self.assertIsNotNone(crit.updated)
        self.assertTrue(crit.active)
    
    def test_clasificacion_hereda_de_modelo_base(self):
        """Verifica que Clasificacion_Sistema hereda campos de ModeloBase"""
        cls = Clasificacion_Sistema.objects.create(code='NET', name='Red')
        
        # Verifica que tiene los campos de ModeloBase
        self.assertIsNotNone(cls.id)
        self.assertIsNotNone(cls.created)
        self.assertIsNotNone(cls.updated)
        self.assertTrue(cls.active)


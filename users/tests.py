from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import (
    Persona, Categoria_Persona, Cargo, 
    Estado_Persona, Nivel_Privilegio
)
from references.models import Departamento
from datetime import date
import uuid


class CategoriaPersonaTests(TestCase):
    """Pruebas unitarias para el modelo Categoria_Persona"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.categoria = Categoria_Persona.objects.create(
            code='EMP',
            name='Empleado'
        )
    
    def test_crear_categoria_persona(self):
        """Verifica que se crea correctamente una Categoria_Persona"""
        self.assertEqual(self.categoria.code, 'EMP')
        self.assertEqual(self.categoria.name, 'Empleado')
    
    def test_categoria_persona_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Categoria_Persona.objects.create(
                code='EMP',
                name='Otra Categoría'
            )
    
    def test_categoria_persona_str(self):
        """Verifica la representación en string"""
        expected_str = "(EMP) Empleado"
        self.assertEqual(str(self.categoria), expected_str)
    
    def test_categoria_persona_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Categoria_Persona._meta
        self.assertEqual(meta.verbose_name, 'Categoria_Persona')
        self.assertEqual(meta.verbose_name_plural, 'Categorias_Personas')


class CargoTests(TestCase):
    """Pruebas unitarias para el modelo Cargo"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.cargo = Cargo.objects.create(
            code='SR',
            name='Senior Developer'
        )
    
    def test_crear_cargo(self):
        """Verifica que se crea correctamente un Cargo"""
        self.assertEqual(self.cargo.code, 'SR')
        self.assertEqual(self.cargo.name, 'Senior Developer')
    
    def test_cargo_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Cargo.objects.create(
                code='SR',
                name='Otro Cargo'
            )
    
    def test_cargo_str(self):
        """Verifica la representación en string"""
        expected_str = "(SR) Senior Developer"
        self.assertEqual(str(self.cargo), expected_str)
    
    def test_cargo_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Cargo._meta
        self.assertEqual(meta.verbose_name, 'Cargo')
        self.assertEqual(meta.verbose_name_plural, 'Cargos')


class EstadoPersonaTests(TestCase):
    """Pruebas unitarias para el modelo Estado_Persona"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.estado = Estado_Persona.objects.create(
            code='ACT',
            name='Activo'
        )
    
    def test_crear_estado_persona(self):
        """Verifica que se crea correctamente un Estado_Persona"""
        self.assertEqual(self.estado.code, 'ACT')
        self.assertEqual(self.estado.name, 'Activo')
    
    def test_estado_persona_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Estado_Persona.objects.create(
                code='ACT',
                name='Otro Estado'
            )
    
    def test_estado_persona_str(self):
        """Verifica la representación en string"""
        expected_str = "(ACT) Activo"
        self.assertEqual(str(self.estado), expected_str)
    
    def test_estado_persona_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Estado_Persona._meta
        self.assertEqual(meta.verbose_name, 'Estado_Persona')
        self.assertEqual(meta.verbose_name_plural, 'Estados_Personas')


class NivelPrivilegioTests(TestCase):
    """Pruebas unitarias para el modelo Nivel_Privilegio"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.nivel = Nivel_Privilegio.objects.create(
            code='USR',
            name='Usuario'
        )
    
    def test_crear_nivel_privilegio(self):
        """Verifica que se crea correctamente un Nivel_Privilegio"""
        self.assertEqual(self.nivel.code, 'USR')
        self.assertEqual(self.nivel.name, 'Usuario')
    
    def test_nivel_privilegio_code_unico(self):
        """Verifica que el campo code es único"""
        with self.assertRaises(IntegrityError):
            Nivel_Privilegio.objects.create(
                code='USR',
                name='Otro Nivel'
            )
    
    def test_nivel_privilegio_str(self):
        """Verifica la representación en string"""
        expected_str = "(USR) Usuario"
        self.assertEqual(str(self.nivel), expected_str)
    
    def test_nivel_privilegio_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Nivel_Privilegio._meta
        self.assertEqual(meta.verbose_name, 'Nivel_Privilegio')
        self.assertEqual(meta.verbose_name_plural, 'Niveles_Privilegios')


class PersonaTests(TestCase):
    """Pruebas unitarias para el modelo Persona"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        # Crear referencias necesarias
        self.departamento = Departamento.objects.create(
            code='IT',
            name='Información y Tecnología'
        )
        self.categoria = Categoria_Persona.objects.create(
            code='EMP',
            name='Empleado'
        )
        self.cargo = Cargo.objects.create(
            code='DEV',
            name='Developer'
        )
        self.estado = Estado_Persona.objects.create(
            code='ACT',
            name='Activo'
        )
        self.nivel = Nivel_Privilegio.objects.create(
            code='USR',
            name='Usuario'
        )
        
        # Crear una Persona
        self.persona = Persona.objects.create(
            identificador_interno='EMP001',
            nombre='Juan',
            apellidos='Garcia Lopez',
            email='juan.garcia@example.com',
            departamento=self.departamento,
            categoria_persona=self.categoria,
            cargo=self.cargo,
            estado_persona=self.estado,
            nivel_privilegio=self.nivel,
            fecha_ingreso=date(2023, 1, 15)
        )
    
    def test_crear_persona(self):
        """Verifica que se crea correctamente una Persona"""
        self.assertEqual(self.persona.identificador_interno, 'EMP001')
        self.assertEqual(self.persona.nombre, 'Juan')
        self.assertEqual(self.persona.apellidos, 'Garcia Lopez')
        self.assertEqual(self.persona.email, 'juan.garcia@example.com')
    
    def test_persona_identificador_interno_unico(self):
        """Verifica que identificador_interno es único"""
        with self.assertRaises(IntegrityError):
            Persona.objects.create(
                identificador_interno='EMP001',  # Duplicado
                nombre='Pedro',
                apellidos='Pérez',
                email='pedro@example.com'
            )
    
    def test_persona_email_unico(self):
        """Verifica que email es único"""
        with self.assertRaises(IntegrityError):
            Persona.objects.create(
                identificador_interno='EMP002',
                nombre='Pedro',
                apellidos='Pérez',
                email='juan.garcia@example.com'  # Duplicado
            )
    
    def test_persona_relaciones_foreignkey(self):
        """Verifica que las relaciones ForeignKey funcionan correctamente"""
        self.assertEqual(self.persona.departamento, self.departamento)
        self.assertEqual(self.persona.categoria_persona, self.categoria)
        self.assertEqual(self.persona.cargo, self.cargo)
        self.assertEqual(self.persona.estado_persona, self.estado)
        self.assertEqual(self.persona.nivel_privilegio, self.nivel)
    
    def test_persona_jefe_directo_opcional(self):
        """Verifica que jefe_directo es opcional (puede ser None)"""
        persona_sin_jefe = Persona.objects.create(
            identificador_interno='EMP003',
            nombre='Maria',
            apellidos='Rodriguez',
            email='maria.rodriguez@example.com'
        )
        self.assertIsNone(persona_sin_jefe.jefe_directo)
    
    def test_persona_jefe_directo_relacion(self):
        """Verifica que jefe_directo establece relación auto-referencial"""
        jefe = Persona.objects.create(
            identificador_interno='EMP002',
            nombre='Carlos',
            apellidos='Lopez',
            email='carlos.lopez@example.com'
        )
        subordinado = Persona.objects.create(
            identificador_interno='EMP004',
            nombre='Ana',
            apellidos='Martinez',
            email='ana.martinez@example.com',
            jefe_directo=jefe
        )
        
        self.assertEqual(subordinado.jefe_directo, jefe)
        self.assertIn(subordinado, jefe.subordinados.all())
    
    def test_persona_fechas_opcionales(self):
        """Verifica que fecha_ingreso y fecha_baja pueden ser vacías"""
        persona = Persona.objects.create(
            identificador_interno='EMP005',
            nombre='Luis',
            apellidos='Diaz',
            email='luis.diaz@example.com'
        )
        self.assertIsNone(persona.fecha_ingreso)
        self.assertIsNone(persona.fecha_baja)
    
    def test_persona_usuario_django_opcional(self):
        """Verifica que usuario_django es opcional"""
        persona = Persona.objects.create(
            identificador_interno='EMP006',
            nombre='Sandra',
            apellidos='Fernandez',
            email='sandra.fernandez@example.com'
        )
        self.assertIsNone(persona.usuario_django)
    
    def test_persona_usuario_django_onetoone(self):
        """Verifica la relación OneToOne con Usuario Django"""
        usuario = User.objects.create_user(
            username='jgarcia',
            password='pass123'
        )
        persona = Persona.objects.create(
            identificador_interno='EMP007',
            nombre='Pablo',
            apellidos='Sanchez',
            email='pablo.sanchez@example.com',
            usuario_django=usuario
        )
        
        self.assertEqual(persona.usuario_django, usuario)
        self.assertEqual(usuario.perfil_persona, persona)
    
    def test_persona_str(self):
        """Verifica la representación en string"""
        expected_str = "Juan Garcia Lopez (EMP001)"
        self.assertEqual(str(self.persona), expected_str)
    
    def test_persona_ordenamiento(self):
        """Verifica que se ordenan por apellidos y nombre"""
        persona1 = Persona.objects.create(
            identificador_interno='EMP008',
            nombre='Andres',
            apellidos='Abrego',
            email='andres.abrego@example.com'
        )
        persona2 = Persona.objects.create(
            identificador_interno='EMP009',
            nombre='Rosa',
            apellidos='Zarate',
            email='rosa.zarate@example.com'
        )
        
        # Obtener todas las personas ordenadas
        personas_ordenadas = list(Persona.objects.all())
        
        # Verificar que estan en el orden correcto: Abrego < Garcia Lopez < Zarate
        apellidos_esperados = ['Abrego', 'Garcia Lopez', 'Zarate']
        apellidos_actuales = [p.apellidos for p in personas_ordenadas]
        self.assertEqual(apellidos_actuales, apellidos_esperados)
    
    def test_persona_verbose_names(self):
        """Verifica los nombres descriptivos en Meta"""
        meta = Persona._meta
        self.assertEqual(meta.verbose_name, 'Persona')
        self.assertEqual(meta.verbose_name_plural, 'Personas')
    
    def test_persona_uuid_primary_key(self):
        """Verifica que el id es un UUID válido"""
        self.assertIsInstance(self.persona.id, uuid.UUID)
    
    def test_persona_timestamps(self):
        """Verifica que created y updated se asignan automáticamente"""
        self.assertIsNotNone(self.persona.created)
        self.assertIsNotNone(self.persona.updated)
    
    def test_persona_active_default(self):
        """Verifica que por defecto active es True"""
        self.assertTrue(self.persona.active)
    
    def test_persona_foreignkey_delete_set_null(self):
        """Verifica que las ForeignKey establecen NULL si se elimina referencia"""
        dept_id = self.persona.departamento.id
        self.persona.departamento.delete()
        
        persona_reload = Persona.objects.get(id=self.persona.id)
        self.assertIsNone(persona_reload.departamento)
    
    def test_persona_actualizar(self):
        """Verifica que se puede actualizar una Persona"""
        self.persona.nombre = 'Juanito'
        self.persona.save()
        
        persona_actualizado = Persona.objects.get(id=self.persona.id)
        self.assertEqual(persona_actualizado.nombre, 'Juanito')
    
    def test_persona_eliminar(self):
        """Verifica que se puede eliminar una Persona"""
        persona_id = self.persona.id
        self.persona.delete()
        
        with self.assertRaises(Persona.DoesNotExist):
            Persona.objects.get(id=persona_id)

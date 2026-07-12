from base.tests.base_test_case import BaseTestSetup
from users.models import Persona, ConfiguracionAltaGerencia
from django.contrib.auth.models import User


class PersonaModelTests(BaseTestSetup):
    def test_crear_persona(self):
        p = Persona.objects.create(
            identificador_interno='TEST-001',
            nombre='Test',
            apellidos='Persona',
        )
        self.assertEqual(p.nombre, 'Test')
        self.assertTrue(p.active)

    def test_persona_str(self):
        p = Persona.objects.create(
            identificador_interno='TEST-002',
            nombre='Juan',
            apellidos='Perez Lopez',
        )
        self.assertIn('Juan', str(p))
        self.assertIn('Perez Lopez', str(p))

    def test_es_alta_gerencia_propiedad_true(self):
        self.assertTrue(self.persona_altagerencia.es_alta_gerencia)

    def test_es_alta_gerencia_propiedad_false(self):
        self.assertFalse(self.persona_supervisor.es_alta_gerencia)

    def test_persona_activa_por_defecto(self):
        p = Persona.objects.create(
            identificador_interno='TEST-003',
            nombre='Default',
            apellidos='Active',
        )
        self.assertTrue(p.active)

    def test_relacion_usuario_django(self):
        self.assertEqual(self.persona_admin.usuario_django, self.user_admin)

    def test_relacion_inversa_user_perfil(self):
        self.assertEqual(self.user_admin.perfil_persona, self.persona_admin)

    def test_soft_delete_persona(self):
        p = Persona.objects.create(
            identificador_interno='TEST-004',
            nombre='ToDelete',
            apellidos='Persona',
            active=True,
        )
        p.active = False
        p.save()
        self.assertFalse(p.active)

    def test_identificador_unico(self):
        Persona.objects.create(identificador_interno='UNICO-01', nombre='A', apellidos='B')
        with self.assertRaises(Exception):
            Persona.objects.create(identificador_interno='UNICO-01', nombre='C', apellidos='D')


class ConfiguracionAltaGerenciaTests(BaseTestSetup):
    def test_crear_configuracion(self):
        config = ConfiguracionAltaGerencia.objects.create(persona=self.persona_altagerencia)
        config.areas_supervision.add(self.area_rectoria)
        self.assertEqual(config.persona, self.persona_altagerencia)
        self.assertIn(self.area_rectoria, config.areas_supervision.all())

    def test_config_sin_areas(self):
        config = ConfiguracionAltaGerencia.objects.create(persona=self.persona_altagerencia)
        self.assertEqual(config.areas_supervision.count(), 0)

from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from users.models import Persona
from django.contrib.auth.models import User


class PersonaViewPermissionTests(BaseTestSetup):
    def test_persona_list_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('persona-lista'))
        self.assertEqual(response.status_code, 200)

    def test_persona_list_supervisor_bloqueado(self):
        self.login_supervisor()
        response = self.client.get(reverse('persona-lista'))
        self.assertNotEqual(response.status_code, 200)

    def test_persona_list_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('persona-lista'))
        self.assertNotEqual(response.status_code, 200)

    def test_persona_create_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('persona-crear'))
        self.assertEqual(response.status_code, 200)

    def test_persona_create_supervisor_bloqueado(self):
        self.login_supervisor()
        response = self.client.get(reverse('persona-crear'))
        self.assertNotEqual(response.status_code, 200)

    def test_persona_detail_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('persona-detalle', args=[self.persona_especialista.pk]))
        self.assertEqual(response.status_code, 200)

    def test_persona_detail_altagerencia_accede(self):
        self.login_altagerencia()
        response = self.client.get(reverse('persona-detalle', args=[self.persona_especialista.pk]))
        self.assertEqual(response.status_code, 200)

    def test_mi_perfil_usuario_accede(self):
        self.login_usuario()
        response = self.client.get(reverse('mi-perfil'))
        self.assertEqual(response.status_code, 200)

    def test_mi_perfil_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('mi-perfil'))
        self.assertEqual(response.status_code, 200)

    def test_persona_eliminar_admin_puede(self):
        p = Persona.objects.create(
            identificador_interno='DEL-001',
            nombre='Delete',
            apellidos='Test',
        )
        self.login_admin()
        response = self.client.post(reverse('persona-eliminar', args=[p.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_persona_reactivar_admin_puede(self):
        p = Persona.objects.create(
            identificador_interno='REACT-001',
            nombre='React',
            apellidos='Test',
        )
        p.active = False
        p.save()
        self.login_admin()
        response = self.client.post(reverse('persona-activar', args=[p.pk]))
        self.assertIn(response.status_code, [200, 302])
        p.refresh_from_db()
        self.assertTrue(p.active)

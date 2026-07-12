from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from incidents.models import Incidente


class SoftDeleteTests(BaseTestSetup):
    def test_eliminar_incidente_soft(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-eliminar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertFalse(inc.active)

    def test_incidente_eliminado_no_aparece_en_lista(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-eliminar', args=[inc.pk]))
        response = self.client.get(reverse('incidente-lista'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertNotIn(inc.titulo, content)

    def test_incidente_eliminado_404_en_detalle(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-eliminar', args=[inc.pk]))
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertEqual(response.status_code, 404)

    def test_incidente_eliminado_aparece_en_eliminados(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-eliminar', args=[inc.pk]))
        response = self.client.get(reverse('incidente-eliminados-lista'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(inc.titulo, content)

    def test_restaurar_incidente_admin(self):
        inc = self.crear_incidente_base()
        inc.active = False
        inc.save()
        self.login_admin()
        self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertTrue(inc.active)

    def test_restaurar_incidente_supervisor_propio(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor)
        inc.active = False
        inc.save()
        self.login_supervisor()
        self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertTrue(inc.active)

    def test_restaurar_incidente_supervisor_ajeno_denied(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor2)
        inc.active = False
        inc.save()
        self.login_supervisor()
        self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertFalse(inc.active)

    def test_supervisor_ve_solo_sus_eliminados(self):
        inc_propio = self.crear_incidente_base(titulo='Propio Eliminado', supervisor=self.persona_supervisor)
        inc_ajeno = self.crear_incidente_base(titulo='Ajeno Eliminado', supervisor=self.persona_supervisor2)
        inc_propio.active = False
        inc_propio.save()
        inc_ajeno.active = False
        inc_ajeno.save()
        self.login_supervisor()
        response = self.client.get(reverse('incidente-eliminados-lista'))
        content = response.content.decode('utf-8')
        self.assertIn('Propio Eliminado', content)
        self.assertNotIn('Ajeno Eliminado', content)

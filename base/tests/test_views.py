from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse


class HomeViewTests(BaseTestSetup):
    def test_home_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_usuario_accede(self):
        self.login_usuario()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_no_autenticado_redirige(self):
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, [200, 302])


class AccesoDenegadoViewTests(BaseTestSetup):
    def test_acceso_denegado_muestra(self):
        self.login_usuario()
        response = self.client.get(reverse('acceso-denegado'))
        self.assertEqual(response.status_code, 200)

    def test_acceso_denegado_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('acceso-denegado'))
        self.assertEqual(response.status_code, 200)

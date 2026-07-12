from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse


class AreaViewTests(BaseTestSetup):
    def test_area_tree_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('area-tree'))
        self.assertEqual(response.status_code, 200)

    def test_area_tree_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('area-tree'))
        self.assertEqual(response.status_code, 200)

    def test_area_tree_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('area-tree'))
        self.assertNotEqual(response.status_code, 200)

    def test_area_tree_especialista_bloqueado(self):
        self.login_especialista()
        response = self.client.get(reverse('area-tree'))
        self.assertNotEqual(response.status_code, 200)

    def test_area_create_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('area-crear'))
        self.assertEqual(response.status_code, 200)

    def test_area_create_supervisor_bloqueado(self):
        self.login_supervisor()
        response = self.client.get(reverse('area-crear'))
        self.assertNotEqual(response.status_code, 200)

    def test_area_update_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('area-detalle', args=[self.area_rectoria.pk]))
        self.assertEqual(response.status_code, 200)

    def test_area_update_supervisor_puede(self):
        self.login_supervisor()
        response = self.client.get(reverse('area-detalle', args=[self.area_rectoria.pk]))
        self.assertEqual(response.status_code, 200)

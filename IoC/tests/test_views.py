from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from IoC.models import IoC


class IoCViewPermissionTests(BaseTestSetup):
    def test_ioc_list_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('ioc-lista'))
        self.assertEqual(response.status_code, 200)

    def test_ioc_list_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('ioc-lista'))
        self.assertEqual(response.status_code, 200)

    def test_ioc_list_especialista_accede(self):
        self.login_especialista()
        response = self.client.get(reverse('ioc-lista'))
        self.assertEqual(response.status_code, 200)

    def test_ioc_list_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('ioc-lista'))
        self.assertNotEqual(response.status_code, 200)

    def test_ioc_create_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('ioc-crear'))
        self.assertEqual(response.status_code, 200)

    def test_ioc_create_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('ioc-crear'))
        self.assertNotEqual(response.status_code, 200)

    def test_ioc_detail_accede(self):
        ioc = IoC.objects.create(tipo_ioc=self.tipo_ioc_ip, valor='4.4.4.4')
        self.login_admin()
        response = self.client.get(reverse('ioc-detalle', args=[ioc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_ioc_edit_accede(self):
        ioc = IoC.objects.create(tipo_ioc=self.tipo_ioc_ip, valor='5.5.5.5')
        self.login_admin()
        response = self.client.get(reverse('ioc-editar', args=[ioc.pk]))
        self.assertEqual(response.status_code, 200)

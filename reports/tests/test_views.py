from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from reports.models import Reporte


class ReporteViewPermissionTests(BaseTestSetup):
    def test_reporte_home_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('reporte-home'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_home_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('reporte-home'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_home_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('reporte-home'))
        self.assertNotEqual(response.status_code, 200)

    def test_reporte_home_altagerencia_accede(self):
        self.login_altagerencia()
        response = self.client.get(reverse('reporte-home'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_list_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('reporte-lista'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_create_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('reporte-crear'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_create_supervisor_puede(self):
        self.login_supervisor()
        response = self.client.get(reverse('reporte-crear'))
        self.assertEqual(response.status_code, 200)

    def test_reporte_create_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('reporte-crear'))
        self.assertNotEqual(response.status_code, 200)

    def test_reporte_detail_admin_accede(self):
        reporte = Reporte.objects.create(
            titulo='Reporte Test',
            tipo_reporte='GEN',
        )
        self.login_admin()
        response = self.client.get(reverse('reporte-detalle', args=[reporte.pk]))
        self.assertEqual(response.status_code, 200)

    def test_incidente_ficha_admin_accede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-ficha', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_incidente_ficha_especialista_asignado_accede(self):
        inc = self.crear_incidente_base(especialista_asignado=self.persona_especialista)
        self.login_especialista()
        response = self.client.get(reverse('incidente-ficha', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

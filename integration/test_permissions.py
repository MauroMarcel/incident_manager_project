from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse


class MatrizPermisosIncidentesTests(BaseTestSetup):
    def test_incidente_list_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('incidente-lista'))
        self.assertEqual(r.status_code, 200)

    def test_incidente_list_supervisor_ok(self):
        self.login_supervisor()
        r = self.client.get(reverse('incidente-lista'))
        self.assertEqual(r.status_code, 200)

    def test_incidente_list_especialista_ok(self):
        self.login_especialista()
        r = self.client.get(reverse('incidente-lista'))
        self.assertEqual(r.status_code, 200)

    def test_incidente_list_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('incidente-lista'))
        self.assertNotEqual(r.status_code, 200)

    def test_incidente_crear_supervisor_ok(self):
        self.login_supervisor()
        r = self.client.get(reverse('incidente-crear-directo'))
        self.assertEqual(r.status_code, 200)

    def test_incidente_crear_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('incidente-crear-directo'))
        self.assertNotEqual(r.status_code, 200)


class MatrizPermisosNotificacionesTests(BaseTestSetup):
    def test_notification_list_usuario_ok(self):
        self.login_usuario()
        r = self.client.get(reverse('notification-list'))
        self.assertEqual(r.status_code, 200)

    def test_notification_list_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('notification-list'))
        self.assertEqual(r.status_code, 200)

    def test_notification_rechazar_usuario_denied(self):
        notif = self.crear_notificacion_base()
        self.login_usuario()
        r = self.client.post(reverse('notification-rechazar', args=[notif.pk]), {'motivo_rechazo': 'x'})
        self.assertNotEqual(r.status_code, 200)

    def test_notification_rechazar_supervisor_ok(self):
        notif = self.crear_notificacion_base()
        self.login_supervisor()
        r = self.client.post(reverse('notification-rechazar', args=[notif.pk]), {'motivo_rechazo': 'x'})
        self.assertIn(r.status_code, [200, 302])


class MatrizPermisosIocTests(BaseTestSetup):
    def test_ioc_list_especialista_ok(self):
        self.login_especialista()
        r = self.client.get(reverse('ioc-lista'))
        self.assertEqual(r.status_code, 200)

    def test_ioc_list_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('ioc-lista'))
        self.assertNotEqual(r.status_code, 200)

    def test_ioc_create_especialista_ok(self):
        self.login_especialista()
        r = self.client.get(reverse('ioc-crear'))
        self.assertEqual(r.status_code, 200)


class MatrizPermisosReportesTests(BaseTestSetup):
    def test_reporte_home_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('reporte-home'))
        self.assertEqual(r.status_code, 200)

    def test_reporte_home_altagerencia_ok(self):
        self.login_altagerencia()
        r = self.client.get(reverse('reporte-home'))
        self.assertEqual(r.status_code, 200)

    def test_reporte_home_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('reporte-home'))
        self.assertNotEqual(r.status_code, 200)


class MatrizPermisosPersonasTests(BaseTestSetup):
    def test_persona_list_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('persona-lista'))
        self.assertEqual(r.status_code, 200)

    def test_persona_list_supervisor_denied(self):
        self.login_supervisor()
        r = self.client.get(reverse('persona-lista'))
        self.assertNotEqual(r.status_code, 200)

    def test_persona_list_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('persona-lista'))
        self.assertNotEqual(r.status_code, 200)

    def test_persona_miperfil_usuario_ok(self):
        self.login_usuario()
        r = self.client.get(reverse('mi-perfil'))
        self.assertEqual(r.status_code, 200)


class MatrizPermisosAreasTests(BaseTestSetup):
    def test_area_tree_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('area-tree'))
        self.assertEqual(r.status_code, 200)

    def test_area_tree_supervisor_ok(self):
        self.login_supervisor()
        r = self.client.get(reverse('area-tree'))
        self.assertEqual(r.status_code, 200)

    def test_area_tree_usuario_denied(self):
        self.login_usuario()
        r = self.client.get(reverse('area-tree'))
        self.assertNotEqual(r.status_code, 200)

    def test_area_crear_admin_ok(self):
        self.login_admin()
        r = self.client.get(reverse('area-crear'))
        self.assertEqual(r.status_code, 200)

    def test_area_crear_supervisor_denied(self):
        self.login_supervisor()
        r = self.client.get(reverse('area-crear'))
        self.assertNotEqual(r.status_code, 200)

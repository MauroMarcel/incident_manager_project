from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from notifications.models import Notificacion


class NotificacionViewPermissionTests(BaseTestSetup):
    def test_notification_list_usuario_accede(self):
        self.login_usuario()
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)

    def test_notification_list_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)

    def test_notification_create_usuario_puede(self):
        self.login_usuario()
        response = self.client.get(reverse('notification-create'))
        self.assertEqual(response.status_code, 200)

    def test_notification_create_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('notification-create'))
        self.assertEqual(response.status_code, 200)

    def test_notification_detail_usuario_ve_propia(self):
        notif = self.crear_notificacion_base(usuario_notificador=self.user_usuario)
        self.login_usuario()
        response = self.client.get(reverse('notification-detail', args=[notif.pk]))
        self.assertEqual(response.status_code, 200)

    def test_notification_rechazar_supervisor_puede(self):
        notif = self.crear_notificacion_base()
        self.login_supervisor()
        response = self.client.post(reverse('notification-rechazar', args=[notif.pk]), {
            'motivo_rechazo': 'No corresponde al area'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_notification_rechazar_usuario_bloqueado(self):
        notif = self.crear_notificacion_base()
        self.login_usuario()
        response = self.client.post(reverse('notification-rechazar', args=[notif.pk]), {
            'motivo_rechazo': 'Test'
        })
        self.assertNotEqual(response.status_code, 200)

    def test_notification_rechazar_actualiza_estado(self):
        notif = self.crear_notificacion_base()
        self.login_supervisor()
        self.client.post(reverse('notification-rechazar', args=[notif.pk]), {
            'motivo_rechazo': 'Incidente duplicado'
        })
        notif.refresh_from_db()
        self.assertEqual(notif.estado_notificacion, self.estado_notif_rec)
        self.assertEqual(notif.respuesta_supervisor, 'Incidente duplicado')

    def test_notification_vincular_admin_puede(self):
        incidente = self.crear_incidente_base()
        notif = self.crear_notificacion_base()
        self.login_admin()
        response = self.client.post(reverse('notificacion-vincular', args=[notif.pk]), {
            'incidente_pk': incidente.pk,
        })
        self.assertIn(response.status_code, [200, 302])

    def test_notification_desvincular_admin_puede(self):
        incidente = self.crear_incidente_base()
        notif = self.crear_notificacion_base(
            incidente_asociado=incidente,
            estado_notificacion=self.estado_notif_ace,
        )
        self.login_admin()
        response = self.client.post(reverse('notificacion-desvincular', args=[notif.pk]))
        self.assertIn(response.status_code, [200, 302])
        notif.refresh_from_db()
        self.assertIsNone(notif.incidente_asociado)
        self.assertEqual(notif.estado_notificacion, self.estado_notif_pen)

from base.tests.base_test_case import BaseTestSetup
from notifications.models import Notificacion


class NotificacionModelTests(BaseTestSetup):
    def test_crear_notificacion(self):
        n = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Asunto Test',
            descripcion='Descripcion test',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
        )
        self.assertEqual(n.asunto, 'Asunto Test')
        self.assertEqual(n.estado_notificacion, self.estado_notif_pen)
        self.assertTrue(n.active)

    def test_notificacion_str(self):
        n = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Incidente de Phishing',
            descripcion='Intento de phishing detectado',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
        )
        self.assertIsNotNone(str(n))

    def test_notificacion_con_respuesta_supervisor(self):
        n = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Respuesta Test',
            descripcion='Test',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_ace,
            respuesta_supervisor='Su incidente ha sido resuelto',
        )
        self.assertEqual(n.respuesta_supervisor, 'Su incidente ha sido resuelto')

    def test_notificacion_con_email_opcional(self):
        n = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Sin Email',
            descripcion='Test sin email',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
            email='',
        )
        self.assertEqual(n.email, '')

    def test_notificacion_orden_por_created(self):
        n1 = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Primera',
            descripcion='Test',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
        )
        n2 = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Segunda',
            descripcion='Test',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
        )
        qs = Notificacion.objects.all()
        self.assertEqual(qs[0], n1)
        self.assertEqual(qs[1], n2)

    def test_cambio_estado_notificacion(self):
        n = Notificacion.objects.create(
            usuario_notificador=self.user_usuario,
            asunto='Cambio Estado',
            descripcion='Test',
            area_notificacion=self.area_rectoria,
            estado_notificacion=self.estado_notif_pen,
        )
        n.estado_notificacion = self.estado_notif_ace
        n.save()
        n.refresh_from_db()
        self.assertEqual(n.estado_notificacion, self.estado_notif_ace)

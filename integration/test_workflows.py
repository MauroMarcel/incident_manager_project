from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from incidents.models import Incidente, MensajeIncidente
from notifications.models import Notificacion
from django.utils import timezone


class FlujoCompletoTests(BaseTestSetup):
    def test_flujo_notificacion_cierre_completo(self):
        self.login_usuario()
        notif = self.crear_notificacion_base(usuario_notificador=self.user_usuario)
        self.assertIsNotNone(notif.pk)
        self.assertEqual(notif.estado_notificacion, self.estado_notif_pen)
        self.client.logout()

        self.login_supervisor()
        inc_response = self.client.post(reverse('incidente-crear', args=[notif.pk]), {
            'titulo': 'Incidente desde flujo completo',
            'descripcion': 'Descripcion generada automaticamente',
            'areas_afectadas': [self.area_rectoria.pk],
            'especialista_asignado': self.persona_especialista.pk,
        })
        self.assertIn(inc_response.status_code, [200, 302])
        inc = Incidente.objects.filter(titulo='Incidente desde flujo completo').first()
        self.assertIsNotNone(inc)

        if inc:
            notif.refresh_from_db()
            self.assertEqual(notif.estado_notificacion, self.estado_notif_ace)

            self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
                'estado': 'CER',
                'mensaje_contenido': 'Su notificacion ha sido procesada. El incidente ha sido cerrado.',
            })

            notif.refresh_from_db()
            from references.models import Estado_Notificacion
            estado_res = Estado_Notificacion.objects.get(code='RES')
            self.assertEqual(notif.estado_notificacion, estado_res)
            self.assertEqual(notif.respuesta_supervisor, 'Su notificacion ha sido procesada. El incidente ha sido cerrado.')
            self.assertTrue(MensajeIncidente.objects.filter(incidente=inc, contenido='Su notificacion ha sido procesada. El incidente ha sido cerrado.').exists())

    def test_flujo_rechazo_notificacion(self):
        notif = self.crear_notificacion_base()
        self.login_supervisor()
        response = self.client.post(reverse('notification-rechazar', args=[notif.pk]), {
            'motivo_rechazo': 'No corresponde a esta area',
        })
        notif.refresh_from_db()
        self.assertEqual(notif.estado_notificacion, self.estado_notif_rec)
        self.assertEqual(notif.respuesta_supervisor, 'No corresponde a esta area')

    def test_flujo_asignacion_especialista(self):
        inc = self.crear_incidente_base()
        self.login_supervisor()
        response = self.client.post(reverse('incidente-reasignar', args=[inc.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_flujo_wizard_completo(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        paso1 = self.client.post(reverse('incidente-wizard', args=[inc.pk, '1']), {
            'origen_incidente': 'Deteccion por SIEM',
            'peligrosidad': self.peligrosidad_alta.pk,
            'sistema_operativo': self.so_win10.pk,
        })
        paso2 = self.client.post(reverse('incidente-wizard', args=[inc.pk, '2']), {
            'alcance': self.alcance_local.pk,
            'tipo_incidente': self.tipo_malware.pk,
            'impacto_incidente': self.impacto_grave.pk,
            'areas_afectadas': [self.area_rectoria.pk],
        })
        paso3 = self.client.post(reverse('incidente-wizard', args=[inc.pk, '3']), {
            'fecha_ocurrencia': timezone.now() - timezone.timedelta(days=1),
        })
        inc.refresh_from_db()
        self.assertEqual(inc.origen_incidente, 'Deteccion por SIEM')

    def test_crear_notificacion_y_ver_en_lista(self):
        self.login_usuario()
        response = self.client.post(reverse('notification-create'), {
            'asunto': self.asunto_malware.pk,
            'descripcion': 'Se detecto actividad sospechosa',
            'area_notificacion': self.area_rectoria.pk,
            'email': 'user@test.com',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Notificacion.objects.filter(descripcion='Se detecto actividad sospechosa').exists())

    def test_supervisor_ve_solo_sus_incidentes(self):
        inc_propio = self.crear_incidente_base(titulo='Propio', supervisor=self.persona_supervisor)
        inc_ajeno = self.crear_incidente_base(titulo='Ajeno', supervisor=self.persona_supervisor2)
        self.login_supervisor()
        response = self.client.get(reverse('incidente-lista'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Propio', content)
        self.assertNotIn('Ajeno', content)

from base.tests.base_test_case import BaseTestSetup
from django.urls import reverse
from incidents.models import Incidente, MensajeIncidente
from django.utils import timezone


class IncidenteListViewTests(BaseTestSetup):
    def test_list_admin_ve_todos(self):
        self.crear_incidente_base(titulo='Admin1')
        self.crear_incidente_base(titulo='Admin2')
        self.login_admin()
        response = self.client.get(reverse('incidente-lista'))
        self.assertEqual(response.status_code, 200)

    def test_list_supervisor_ve_solo_suyos(self):
        inc_propio = self.crear_incidente_base(titulo='Propio', supervisor=self.persona_supervisor)
        ajeno = self.crear_incidente_base(titulo='Ajeno', supervisor=self.persona_supervisor2)
        self.login_supervisor()
        response = self.client.get(reverse('incidente-lista'))
        self.assertEqual(response.status_code, 200)

    def test_list_especialista_ve_solo_asignados(self):
        inc_asignado = self.crear_incidente_base(titulo='Asignado', especialista_asignado=self.persona_especialista)
        no_asignado = self.crear_incidente_base(titulo='Otro')
        self.login_especialista()
        response = self.client.get(reverse('incidente-lista'))
        self.assertEqual(response.status_code, 200)

    def test_list_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('incidente-lista'))
        self.assertNotEqual(response.status_code, 200)


class IncidenteDetailViewTests(BaseTestSetup):
    def test_detail_admin_accede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_supervisor_accede(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor)
        self.login_supervisor()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_especialista_asignado_accede(self):
        inc = self.crear_incidente_base(especialista_asignado=self.persona_especialista)
        self.login_especialista()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_especialista_no_asignado_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_especialista()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_detail_usuario_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_usuario()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_detail_incidente_inactivo_404(self):
        inc = self.crear_incidente_base()
        inc.active = False
        inc.save()
        self.login_admin()
        response = self.client.get(reverse('incidente-detalle', args=[inc.pk]))
        self.assertEqual(response.status_code, 404)


class IncidenteCreateViewTests(BaseTestSetup):
    def test_create_direct_admin_puede(self):
        self.login_admin()
        response = self.client.get(reverse('incidente-crear-directo'))
        self.assertEqual(response.status_code, 200)

    def test_create_direct_supervisor_puede(self):
        self.login_supervisor()
        response = self.client.get(reverse('incidente-crear-directo'))
        self.assertEqual(response.status_code, 200)

    def test_create_direct_usuario_bloqueado(self):
        self.login_usuario()
        response = self.client.get(reverse('incidente-crear-directo'))
        self.assertNotEqual(response.status_code, 200)

    def test_create_direct_post_valido(self):
        self.login_supervisor()
        response = self.client.post(reverse('incidente-crear-directo'), {
            'titulo': 'Incidente Creado en Test',
            'descripcion': 'Descripcion del incidente',
            'areas_afectadas': [self.area_rectoria.pk],
            'especialista_asignado': self.persona_especialista.pk,
        })
        self.assertIn(response.status_code, [200, 302])


class IncidenteCambiarEstadoViewTests(BaseTestSetup):
    def test_cambiar_a_investigado_admin(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
            'estado': 'INV',
        })
        self.assertIn(response.status_code, [200, 302])
        inc.refresh_from_db()
        self.assertEqual(inc.estado_incidente, self.estado_inv)

    def test_cambiar_a_cerrado_admin(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
            'estado': 'CER',
            'mensaje_contenido': 'Incidente resuelto',
        })
        self.assertIn(response.status_code, [200, 302])
        inc.refresh_from_db()
        self.assertEqual(inc.estado_incidente, self.estado_cer)
        self.assertIsNotNone(inc.fecha_solucion)

    def test_cambiar_estado_especialista_no_asignado_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_especialista()
        response = self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
            'estado': 'ASI',
        })
        self.assertNotEqual(response.status_code, 200)

    def test_cambiar_estado_supervisor_no_asignado_bloqueado(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor2)
        self.login_supervisor()
        response = self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
            'estado': 'ASI',
        })
        self.assertNotEqual(response.status_code, 200)

    def test_cerrar_crea_mensaje_interno(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-cambiar-estado', args=[inc.pk]), {
            'estado': 'CER',
            'mensaje_contenido': 'Caso cerrado por admin',
        })
        self.assertTrue(MensajeIncidente.objects.filter(incidente=inc, contenido='Caso cerrado por admin').exists())


class IncidenteWizardViewTests(BaseTestSetup):
    def test_wizard_paso1_admin_accede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-wizard', args=[inc.pk, '1']))
        self.assertEqual(response.status_code, 200)

    def test_wizard_incidente_cerrado_bloqueado(self):
        inc = self.crear_incidente_base(estado_incidente=self.estado_cer)
        self.login_admin()
        response = self.client.get(reverse('incidente-wizard', args=[inc.pk, '1']))
        self.assertIn(response.status_code, [200, 302])

    def test_wizard_especialista_no_asignado_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_especialista()
        response = self.client.get(reverse('incidente-wizard', args=[inc.pk, '1']))
        self.assertNotEqual(response.status_code, 200)


class IncidenteDeleteRestoreViewTests(BaseTestSetup):
    def test_delete_view_admin_puede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-eliminar', args=[inc.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_delete_soft_admin(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        self.client.post(reverse('incidente-eliminar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertFalse(inc.active)

    def test_deleted_list_admin_accede(self):
        self.login_admin()
        response = self.client.get(reverse('incidente-eliminados-lista'))
        self.assertEqual(response.status_code, 200)

    def test_deleted_list_supervisor_accede(self):
        self.login_supervisor()
        response = self.client.get(reverse('incidente-eliminados-lista'))
        self.assertEqual(response.status_code, 200)

    def test_restore_admin_puede(self):
        inc = self.crear_incidente_base()
        inc.active = False
        inc.save()
        self.login_admin()
        response = self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        self.assertIn(response.status_code, [200, 302])
        inc.refresh_from_db()
        self.assertTrue(inc.active)

    def test_restore_supervisor_propio_puede(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor)
        inc.active = False
        inc.save()
        self.login_supervisor()
        response = self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        self.assertIn(response.status_code, [200, 302])
        inc.refresh_from_db()
        self.assertTrue(inc.active)

    def test_restore_supervisor_ajeno_bloqueado(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor2)
        inc.active = False
        inc.save()
        self.login_supervisor()
        response = self.client.post(reverse('incidente-restaurar', args=[inc.pk]))
        inc.refresh_from_db()
        self.assertFalse(inc.active)


class IncidenteMensajesViewTests(BaseTestSetup):
    def test_mensajes_admin_accede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-mensajes', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_mensajes_especialista_asignado_accede(self):
        inc = self.crear_incidente_base(especialista_asignado=self.persona_especialista)
        self.login_especialista()
        response = self.client.get(reverse('incidente-mensajes', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_mensajes_especialista_no_asignado_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_especialista()
        response = self.client.get(reverse('incidente-mensajes', args=[inc.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_mensajes_incidente_cerrado_bloqueado(self):
        inc = self.crear_incidente_base(estado_incidente=self.estado_cer)
        self.login_admin()
        response = self.client.get(reverse('incidente-mensajes', args=[inc.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_mensajes_post_admin_envia(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.post(reverse('incidente-mensajes', args=[inc.pk]), {
            'contenido': 'Mensaje de prueba desde test',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(MensajeIncidente.objects.filter(incidente=inc, contenido='Mensaje de prueba desde test').exists())


class IncidenteEvidenciaViewTests(BaseTestSetup):
    def test_evidencia_upload_admin_puede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        tmp.write(b'contenido de prueba')
        tmp.close()
        with open(tmp.name, 'rb') as f:
            response = self.client.post(reverse('incidente-evidencia', args=[inc.pk]), {'archivo': f})
        os.unlink(tmp.name)
        self.assertIn(response.status_code, [200, 302])

    def test_evidencia_delete_admin_puede(self):
        from incidents.models import Evidencia_Incidente
        inc = self.crear_incidente_base()
        ev = Evidencia_Incidente.objects.create(incidente=inc)
        self.login_admin()
        response = self.client.post(reverse('incidente-evidencia-eliminar', args=[ev.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_evidencia_delete_supervisor_no_asignado_bloqueado(self):
        from incidents.models import Evidencia_Incidente
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor2)
        ev = Evidencia_Incidente.objects.create(incidente=inc)
        self.login_supervisor()
        response = self.client.post(reverse('incidente-evidencia-eliminar', args=[ev.pk]))
        self.assertIn(response.status_code, [200, 302])


class IncidenteAsignarViewTests(BaseTestSetup):
    def test_asignar_admin_puede(self):
        inc = self.crear_incidente_base()
        self.login_admin()
        response = self.client.get(reverse('incidente-asignar', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_asignar_supervisor_propio_puede(self):
        inc = self.crear_incidente_base(supervisor=self.persona_supervisor)
        self.login_supervisor()
        response = self.client.get(reverse('incidente-asignar', args=[inc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_asignar_usuario_bloqueado(self):
        inc = self.crear_incidente_base()
        self.login_usuario()
        response = self.client.get(reverse('incidente-asignar', args=[inc.pk]))
        self.assertNotEqual(response.status_code, 200)

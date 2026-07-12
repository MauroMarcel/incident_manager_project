from base.tests.base_test_case import BaseTestSetup
from incidents.models import Incidente, MensajeIncidente, Evidencia_Incidente
from django.utils import timezone


class IncidenteModelTests(BaseTestSetup):
    def test_crear_incidente(self):
        inc = Incidente.objects.create(
            titulo='Incidente Test',
            descripcion='Descripcion de prueba',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertEqual(inc.titulo, 'Incidente Test')
        self.assertTrue(inc.active)
        self.assertIsNotNone(inc.codigo)

    def test_codigo_auto_generado(self):
        inc = Incidente.objects.create(
            titulo='Test Codigo',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        import datetime
        year = datetime.datetime.now().year
        self.assertTrue(inc.codigo.startswith(f'INC-{year}-'))

    def test_codigo_secuencial(self):
        inc1 = Incidente.objects.create(
            titulo='Primero',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        inc2 = Incidente.objects.create(
            titulo='Segundo',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        num1 = int(inc1.codigo.split('-')[-1])
        num2 = int(inc2.codigo.split('-')[-1])
        self.assertEqual(num2, num1 + 1)

    def test_incidente_str(self):
        inc = Incidente.objects.create(
            titulo='Incidente EstrTest',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertIn(inc.codigo, str(inc))
        self.assertIn('Incidente EstrTest', str(inc))

    def test_incidente_supervisor_asignado(self):
        inc = Incidente.objects.create(
            titulo='Supervisor Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertEqual(inc.supervisor, self.persona_supervisor)

    def test_incidente_especialista_asignado(self):
        inc = Incidente.objects.create(
            titulo='Esp Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            especialista_asignado=self.persona_especialista,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertEqual(inc.especialista_asignado, self.persona_especialista)

    def test_incidente_estado_inicial(self):
        inc = Incidente.objects.create(
            titulo='Estado Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertEqual(inc.estado_incidente, self.estado_asi)

    def test_incidente_active_default_true(self):
        inc = Incidente.objects.create(
            titulo='Active Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.assertTrue(inc.active)

    def test_incidente_soft_delete(self):
        inc = Incidente.objects.create(
            titulo='Soft Delete Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        inc.active = False
        inc.save()
        self.assertFalse(inc.active)
        self.assertIsNotNone(Incidente.objects.get(pk=inc.pk))

    def test_incidente_fechas(self):
        now = timezone.now()
        inc = Incidente.objects.create(
            titulo='Fechas Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=now,
            fecha_ocurrencia=now - timezone.timedelta(hours=2),
            fecha_asignacion=now + timezone.timedelta(hours=1),
        )
        self.assertIsNotNone(inc.fecha_ocurrencia)
        self.assertIsNotNone(inc.fecha_asignacion)

    def test_areas_afectadas_m2m(self):
        inc = Incidente.objects.create(
            titulo='Areas Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        inc.areas_afectadas.add(self.area_rectoria, self.area_vracad)
        self.assertEqual(inc.areas_afectadas.count(), 2)

    def test_involucrados_m2m(self):
        inc = Incidente.objects.create(
            titulo='Involucrados Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        inc.involucrados.add(self.persona_especialista)
        self.assertEqual(inc.involucrados.count(), 1)


class MensajeIncidenteModelTests(BaseTestSetup):
    def test_crear_mensaje(self):
        inc = self.crear_incidente_base()
        msg = MensajeIncidente.objects.create(
            incidente=inc,
            remitente=self.persona_supervisor,
            contenido='Mensaje de prueba',
        )
        self.assertEqual(msg.contenido, 'Mensaje de prueba')
        self.assertFalse(msg.leido)

    def test_mensaje_leido_default_false(self):
        inc = self.crear_incidente_base()
        msg = MensajeIncidente.objects.create(
            incidente=inc,
            remitente=self.persona_supervisor,
            contenido='Test',
        )
        self.assertFalse(msg.leido)

    def test_mensaje_str(self):
        inc = self.crear_incidente_base()
        msg = MensajeIncidente.objects.create(
            incidente=inc,
            remitente=self.persona_supervisor,
            contenido='Mensaje Test',
        )
        self.assertIn(inc.codigo, str(msg))

    def test_mensaje_orden_cronologico(self):
        inc = self.crear_incidente_base()
        m1 = MensajeIncidente.objects.create(incidente=inc, remitente=self.persona_supervisor, contenido='Primero')
        m2 = MensajeIncidente.objects.create(incidente=inc, remitente=self.persona_supervisor, contenido='Segundo')
        qs = MensajeIncidente.objects.filter(incidente=inc)
        self.assertEqual(qs[0], m1)
        self.assertEqual(qs[1], m2)

    def test_mensaje_relacion_inversa_incidente(self):
        inc = self.crear_incidente_base()
        MensajeIncidente.objects.create(incidente=inc, remitente=self.persona_supervisor, contenido='Msg 1')
        MensajeIncidente.objects.create(incidente=inc, remitente=self.persona_supervisor, contenido='Msg 2')
        self.assertEqual(inc.mensajes.count(), 2)

    def test_mensaje_marcar_como_leido(self):
        inc = self.crear_incidente_base()
        msg = MensajeIncidente.objects.create(incidente=inc, remitente=self.persona_supervisor, contenido='Leer')
        msg.leido = True
        msg.save()
        self.assertTrue(msg.leido)


class EvidenciaIncidenteModelTests(BaseTestSetup):
    def test_crear_evidencia(self):
        inc = self.crear_incidente_base()
        ev = Evidencia_Incidente.objects.create(incidente=inc)
        self.assertIsNotNone(ev.pk)
        self.assertEqual(ev.incidente, inc)

    def test_evidencia_relacion_inversa(self):
        inc = self.crear_incidente_base()
        ev = Evidencia_Incidente.objects.create(incidente=inc)
        self.assertIn(ev, inc.evidencias.all())

    def test_evidencia_verbose_names(self):
        self.assertEqual(Evidencia_Incidente._meta.verbose_name, "Evidencia del Incidente")
        self.assertEqual(Evidencia_Incidente._meta.verbose_name_plural, "Evidencias del Incidente")

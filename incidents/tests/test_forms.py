from base.tests.base_test_case import BaseTestSetup
from incidents.forms import (
    IncidenteTemporalidadForm, MensajeIncidenteForm,
    IncidenteForm, IncidenteReporteOficialForm, IncidenteClasificacionInternaForm
)
from incidents.models import Incidente
from django.utils import timezone


class IncidenteTemporalidadFormTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.inc = Incidente.objects.create(
            titulo='Temporalidad Test',
            descripcion='Test',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )

    def test_form_valido_sin_fechas(self):
        form = IncidenteTemporalidadForm(instance=self.inc, data={})
        self.assertTrue(form.is_valid())

    def test_form_valido_con_fechas_correctas(self):
        now = timezone.now()
        form = IncidenteTemporalidadForm(instance=self.inc, data={
            'fecha_ocurrencia': now - timezone.timedelta(hours=2),
            'fecha_solucion': now + timezone.timedelta(hours=1),
        })
        self.assertTrue(form.is_valid())

    def test_fecha_inicio_mayor_que_cierre_invalido(self):
        now = timezone.now()
        form = IncidenteTemporalidadForm(instance=self.inc, data={
            'fecha_ocurrencia': now + timezone.timedelta(hours=2),
            'fecha_solucion': now + timezone.timedelta(hours=1),
        })
        self.assertFalse(form.is_valid())

    def test_fecha_inicio_mayor_que_reporte_invalido(self):
        form = IncidenteTemporalidadForm(instance=self.inc, data={
            'fecha_ocurrencia': self.inc.fecha_reportado + timezone.timedelta(hours=1),
            'fecha_solucion': '',
        })
        self.assertFalse(form.is_valid())

    def test_fecha_cierre_anterior_a_reporte_invalido(self):
        now = timezone.now()
        self.inc.fecha_reportado = now + timezone.timedelta(hours=3)
        self.inc.save()
        form = IncidenteTemporalidadForm(instance=self.inc, data={
            'fecha_ocurrencia': now,
            'fecha_solucion': now + timezone.timedelta(hours=1),
        })
        self.assertFalse(form.is_valid())

    def test_fecha_asignacion_mayor_que_cierre_invalido(self):
        now = timezone.now()
        self.inc.fecha_asignacion = now + timezone.timedelta(hours=3)
        self.inc.save()
        form = IncidenteTemporalidadForm(instance=self.inc, data={
            'fecha_ocurrencia': now,
            'fecha_solucion': now + timezone.timedelta(hours=1),
        })
        self.assertFalse(form.is_valid())

    def test_labels_actualizados(self):
        form = IncidenteTemporalidadForm(instance=self.inc)
        self.assertEqual(form.fields['fecha_ocurrencia'].label, 'Fecha de inicio')
        self.assertEqual(form.fields['fecha_solucion'].label, 'Fecha de cierre')


class MensajeIncidenteFormTests(BaseTestSetup):
    def test_form_valido(self):
        form = MensajeIncidenteForm(data={'contenido': 'Mensaje de prueba'})
        self.assertTrue(form.is_valid())

    def test_form_contenido_requerido(self):
        form = MensajeIncidenteForm(data={'contenido': ''})
        self.assertFalse(form.is_valid())

    def test_form_label_vacio(self):
        form = MensajeIncidenteForm()
        self.assertEqual(form.fields['contenido'].label, '')


class IncidenteFormTests(BaseTestSetup):
    def test_form_fields_exist(self):
        form = IncidenteForm()
        expected = {'titulo', 'descripcion', 'areas_afectadas', 'especialista_asignado'}
        self.assertEqual(set(form.fields.keys()), expected)


class IncidenteReporteOficialFormTests(BaseTestSetup):
    def test_form_fields_exist(self):
        form = IncidenteReporteOficialForm()
        self.assertIn('origen_incidente', form.fields)
        self.assertIn('peligrosidad', form.fields)
        self.assertIn('subcategoria', form.fields)

    def test_labels_personalizados(self):
        form = IncidenteReporteOficialForm()
        self.assertEqual(form.fields['origen_incidente'].label, 'Origen del incidente')


class IncidenteClasificacionInternaFormTests(BaseTestSetup):
    def test_form_fields_exist(self):
        form = IncidenteClasificacionInternaForm()
        self.assertIn('alcance', form.fields)
        self.assertIn('tipo_incidente', form.fields)
        self.assertIn('impacto_incidente', form.fields)

    def test_labels_personalizados(self):
        form = IncidenteClasificacionInternaForm()
        self.assertEqual(form.fields['indicador_compromiso'].label, 'Indicador(es) de compromiso')

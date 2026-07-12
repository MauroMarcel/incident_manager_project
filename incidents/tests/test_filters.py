from base.tests.base_test_case import BaseTestSetup
from incidents.filters import IncidenteFilter
from incidents.models import Incidente
from django.utils import timezone


class IncidenteFilterTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.inc1 = Incidente.objects.create(
            titulo='Phishing en Rectoria',
            descripcion='Intento de phishing',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_asi,
            fecha_reportado=timezone.now(),
        )
        self.inc1.areas_afectadas.add(self.area_rectoria)

        self.inc2 = Incidente.objects.create(
            titulo='Malware en VRACAD',
            descripcion='Deteccion de malware',
            supervisor=self.persona_supervisor,
            estado_incidente=self.estado_inv,
            especialista_asignado=self.persona_especialista,
            fecha_reportado=timezone.now(),
        )
        self.inc2.areas_afectadas.add(self.area_vracad)

    def test_filtro_sin_parametros(self):
        qs = Incidente.objects.filter(active=True)
        f = IncidenteFilter(data={}, queryset=qs)
        self.assertEqual(f.qs.count(), 2)

    def test_filtro_por_estado(self):
        qs = Incidente.objects.filter(active=True)
        f = IncidenteFilter(data={'estado_incidente': self.estado_inv.pk}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first(), self.inc2)

    def test_filtro_por_area(self):
        qs = Incidente.objects.filter(active=True)
        f = IncidenteFilter(data={'areas_afectadas': [self.area_rectoria.pk]}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)

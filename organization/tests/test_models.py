from base.tests.base_test_case import BaseTestSetup
from organization.models import Area


class AreaModelTests(BaseTestSetup):
    def test_crear_area_raiz(self):
        area = Area.objects.create(nombre='Area Test Raiz')
        self.assertEqual(area.nombre, 'Area Test Raiz')
        self.assertIsNone(area.area_superior)

    def test_crear_subarea(self):
        sub = Area.objects.create(nombre='Subarea', area_superior=self.area_rectoria)
        self.assertEqual(sub.area_superior, self.area_rectoria)

    def test_relacion_subareas(self):
        sub = Area.objects.create(nombre='Subarea2', area_superior=self.area_rectoria)
        self.assertIn(sub, self.area_rectoria.subareas.all())

    def test_area_str(self):
        self.assertEqual(str(self.area_rectoria), 'Rectoria')

    def test_subarea_str(self):
        sub = Area.objects.create(nombre='Subarea3', area_superior=self.area_rectoria)
        self.assertIn('Subarea3', str(sub))

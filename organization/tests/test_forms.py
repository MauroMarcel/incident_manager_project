from base.tests.base_test_case import BaseTestSetup
from organization.forms import AreaForm
from organization.models import Area


class AreaFormTests(BaseTestSetup):
    def test_form_valido(self):
        form = AreaForm(data={'nombre': 'Nueva Area', 'area_superior': ''})
        self.assertTrue(form.is_valid())

    def test_form_con_area_superior(self):
        form = AreaForm(data={'nombre': 'Subarea', 'area_superior': self.area_rectoria.pk})
        self.assertTrue(form.is_valid())

    def test_form_nombre_requerido(self):
        form = AreaForm(data={'nombre': '', 'area_superior': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_form_nombre_duplicado_bajo_mismo_padre(self):
        Area.objects.create(nombre='Duplicado', area_superior=self.area_rectoria)
        form = AreaForm(data={'nombre': 'Duplicado', 'area_superior': self.area_rectoria.pk})
        self.assertFalse(form.is_valid())

    def test_form_mismo_nombre_raiz_ok(self):
        Area.objects.create(nombre='Unico')
        form = AreaForm(data={'nombre': 'Unico', 'area_superior': self.area_rectoria.pk})
        self.assertTrue(form.is_valid())

    def test_form_circular_reference(self):
        sub = Area.objects.create(nombre='Sub', area_superior=self.area_rectoria)
        form = AreaForm(data={'nombre': 'Modificado', 'area_superior': sub.pk}, instance=self.area_rectoria)
        self.assertFalse(form.is_valid())

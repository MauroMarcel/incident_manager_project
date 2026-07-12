from base.tests.base_test_case import BaseTestSetup
from base.utils import get_areas_supervision, get_areas_recursivas
from users.models import ConfiguracionAltaGerencia
from organization.models import Area


class UtilsTests(BaseTestSetup):
    def test_get_areas_supervision_sin_config(self):
        areas = get_areas_supervision(self.persona_supervisor)
        self.assertEqual(len(areas), 0)

    def test_get_areas_supervision_con_config(self):
        config = ConfiguracionAltaGerencia.objects.create(persona=self.persona_altagerencia)
        config.areas_supervision.add(self.area_rectoria)
        areas = get_areas_supervision(self.persona_altagerencia)
        self.assertIn(self.area_rectoria, areas)

    def test_get_areas_supervision_con_subareas(self):
        config = ConfiguracionAltaGerencia.objects.create(persona=self.persona_altagerencia)
        config.areas_supervision.add(self.area_rectoria)
        sub = Area.objects.create(nombre='Subarea', area_superior=self.area_rectoria)
        areas = get_areas_supervision(self.persona_altagerencia)
        self.assertIn(sub, areas)

    def test_get_areas_recursivas_raiz(self):
        sub = Area.objects.create(nombre='Sub', area_superior=self.area_rectoria)
        sub2 = Area.objects.create(nombre='Sub2', area_superior=sub)
        result = get_areas_recursivas(self.area_rectoria)
        self.assertIn(self.area_rectoria, result)
        self.assertIn(sub, result)
        self.assertIn(sub2, result)

    def test_get_areas_recursivas_sin_subareas(self):
        area = Area.objects.create(nombre='Aislada')
        result = get_areas_recursivas(area)
        self.assertEqual(len(result), 1)
        self.assertIn(area, result)

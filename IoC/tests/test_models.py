from base.tests.base_test_case import BaseTestSetup
from IoC.models import IoC


class IoCModelTests(BaseTestSetup):
    def test_creacion_ioc(self):
        ioc = IoC.objects.create(
            tipo_ioc=self.tipo_ioc_ip,
            valor='192.168.1.100',
            descripcion='IP maliciosa'
        )
        self.assertEqual(ioc.valor, '192.168.1.100')
        self.assertEqual(ioc.tipo_ioc, self.tipo_ioc_ip)
        self.assertIn('192.168.1.100', str(ioc))

    def test_ioc_sin_descripcion(self):
        ioc = IoC.objects.create(
            tipo_ioc=self.tipo_ioc_ip,
            valor='10.0.0.1'
        )
        self.assertIsNone(ioc.descripcion)

    def test_ioc_str(self):
        ioc = IoC.objects.create(
            tipo_ioc=self.tipo_ioc_ip,
            valor='8.8.8.8'
        )
        self.assertIn('8.8.8.8', str(ioc))

    def test_verbose_names(self):
        self.assertEqual(IoC._meta.verbose_name, "Indicador de Compromiso (IOC)")
        self.assertEqual(IoC._meta.verbose_name_plural, "Indicadores de Compromiso (IOCs)")

    def test_ioc_active_default(self):
        ioc = IoC.objects.create(
            tipo_ioc=self.tipo_ioc_ip,
            valor='1.1.1.1'
        )
        self.assertTrue(ioc.active)

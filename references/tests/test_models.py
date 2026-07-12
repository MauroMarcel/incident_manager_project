from base.tests.base_test_case import BaseTestSetup
from references.models import (
    Estado_Incidente, Estado_Notificacion, Prioridad, Impacto_Incidente,
    Tipo_Incidente, Alcance, Vector_Ataque, Fuente_Deteccion, Tecnologia,
    Intencionalidad, Peligrosidad, Sistema_Operativo, Tipo_IOC,
    Asunto_Notificacion, Categoria_Persona, Cargo, Estado_Persona
)


class NomencladorModelTests(BaseTestSetup):
    def test_crear_estado_incidente(self):
        estado = Estado_Incidente.objects.create(code='PRB', name='Prueba')
        self.assertEqual(estado.code, 'PRB')
        self.assertEqual(estado.name, 'Prueba')
        self.assertTrue(estado.active)

    def test_crear_estado_notificacion(self):
        estado = Estado_Notificacion.objects.create(code='PRB', name='Prueba')
        self.assertEqual(str(estado), '(PRB) Prueba')

    def test_crear_prioridad(self):
        p = Prioridad.objects.create(code='PRB', name='Prueba')
        self.assertEqual(p.code, 'PRB')

    def test_crear_impacto_incidente(self):
        obj = Impacto_Incidente.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.name, 'Prueba')
        self.assertTrue(obj.active)

    def test_crear_tipo_incidente(self):
        obj = Tipo_Incidente.objects.create(code='PRB', name='Prueba')
        self.assertIn('PRB', str(obj))

    def test_crear_alcance(self):
        obj = Alcance.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.code, 'PRB')

    def test_crear_vector_ataque(self):
        obj = Vector_Ataque.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.name, 'Prueba')

    def test_crear_fuente_deteccion(self):
        obj = Fuente_Deteccion.objects.create(code='PRB', name='Prueba')
        self.assertTrue(obj.active)

    def test_crear_tecnologia(self):
        obj = Tecnologia.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.code, 'PRB')

    def test_crear_intencionalidad(self):
        obj = Intencionalidad.objects.create(code='PRB', name='Prueba')
        self.assertEqual(str(obj), '(PRB) Prueba')

    def test_crear_peligrosidad(self):
        obj = Peligrosidad.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.name, 'Prueba')

    def test_crear_sistema_operativo(self):
        obj = Sistema_Operativo.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.code, 'PRB')

    def test_crear_tipo_ioc(self):
        obj = Tipo_IOC.objects.create(code='PRB', name='Prueba')
        self.assertTrue(obj.active)

    def test_crear_asunto_notificacion(self):
        obj = Asunto_Notificacion.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.code, 'PRB')

    def test_crear_categoria_persona(self):
        obj = Categoria_Persona.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.name, 'Prueba')

    def test_crear_cargo(self):
        obj = Cargo.objects.create(code='PRB', name='Prueba')
        self.assertTrue(obj.active)

    def test_crear_estado_persona(self):
        obj = Estado_Persona.objects.create(code='PRB', name='Prueba')
        self.assertEqual(obj.code, 'PRB')

    def test_code_unique(self):
        with self.assertRaises(Exception):
            Estado_Incidente.objects.create(code='ASI', name='Duplicado')

    def test_estados_semilla_existen(self):
        self.assertEqual(Estado_Incidente.objects.get(code='ASI').name, 'Asignado')
        self.assertEqual(Estado_Incidente.objects.get(code='INV').name, 'En Investigacion')
        self.assertEqual(Estado_Incidente.objects.get(code='CER').name, 'Cerrado')
        self.assertEqual(Estado_Notificacion.objects.get(code='PEN').name, 'Pendiente')
        self.assertEqual(Estado_Notificacion.objects.get(code='ACE').name, 'Aceptada')
        self.assertEqual(Estado_Notificacion.objects.get(code='REC').name, 'Rechazada')

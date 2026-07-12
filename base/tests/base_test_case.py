from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from references.models import (
    Estado_Incidente, Estado_Notificacion, Asunto_Notificacion,
    Estado_Persona, Categoria_Persona, Cargo,
    Prioridad, Impacto_Incidente, Tipo_Incidente, Alcance,
    Vector_Ataque, Fuente_Deteccion, Tecnologia, Intencionalidad,
    Peligrosidad, Sistema_Operativo, Tipo_IOC, Categoria, Subcategoria
)
from organization.models import Area
from users.models import Persona


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._crear_grupos()
        cls._crear_nomencladores()
        cls._crear_areas()
        cls._crear_usuarios_y_personas()

    @classmethod
    def _crear_grupos(cls):
        grupos = ['Administrador', 'Supervisor', 'Especialista', 'Usuario', 'Alta Gerencia']
        cls.grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
        cls.grupo_supervisor, _ = Group.objects.get_or_create(name='Supervisor')
        cls.grupo_especialista, _ = Group.objects.get_or_create(name='Especialista')
        cls.grupo_usuario, _ = Group.objects.get_or_create(name='Usuario')
        cls.grupo_alta_gerencia, _ = Group.objects.get_or_create(name='Alta Gerencia')

    @classmethod
    def _crear_nomencladores(cls):
        cls.estado_asi, _ = Estado_Incidente.objects.get_or_create(code='ASI', name='Asignado')
        cls.estado_inv, _ = Estado_Incidente.objects.get_or_create(code='INV', name='En Investigacion')
        cls.estado_cer, _ = Estado_Incidente.objects.get_or_create(code='CER', name='Cerrado')

        cls.estado_notif_pen, _ = Estado_Notificacion.objects.get_or_create(code='PEN', name='Pendiente')
        cls.estado_notif_ace, _ = Estado_Notificacion.objects.get_or_create(code='ACE', name='Aceptada')
        cls.estado_notif_rec, _ = Estado_Notificacion.objects.get_or_create(code='REC', name='Rechazada')

        cls.estado_persona_act, _ = Estado_Persona.objects.get_or_create(code='ACT', name='Activo')
        cls.estado_persona_ina, _ = Estado_Persona.objects.get_or_create(code='INA', name='Inactivo')

        cls.categoria_adm, _ = Categoria_Persona.objects.get_or_create(code='ADM', name='Administrativo')
        cls.cargo_esp, _ = Cargo.objects.get_or_create(code='ESP', name='Especialista')
        cls.cargo_sup, _ = Cargo.objects.get_or_create(code='SPV', name='Supervisor')

        cls.prioridad_alta, _ = Prioridad.objects.get_or_create(code='ALT', name='Alta')
        cls.impacto_grave, _ = Impacto_Incidente.objects.get_or_create(code='GRA', name='Grave')
        cls.tipo_malware, _ = Tipo_Incidente.objects.get_or_create(code='MAL', name='Malware')
        cls.alcance_local, _ = Alcance.objects.get_or_create(code='LOC', name='Local')
        cls.vector_email, _ = Vector_Ataque.objects.get_or_create(code='EMA', name='Correo Electronico')
        cls.fuente_siem, _ = Fuente_Deteccion.objects.get_or_create(code='SIEM', name='SIEM')
        cls.tecnologia_win, _ = Tecnologia.objects.get_or_create(code='WIN', name='Windows')
        cls.intencionalidad_int, _ = Intencionalidad.objects.get_or_create(code='INT', name='Intencional')
        cls.peligrosidad_alta, _ = Peligrosidad.objects.get_or_create(code='ALT', name='Alta')
        cls.so_win10, _ = Sistema_Operativo.objects.get_or_create(code='WIN10', name='Windows 10')
        cls.tipo_ioc_ip, _ = Tipo_IOC.objects.get_or_create(code='IP', name='Direccion IP')
        cls.asunto_malware, _ = Asunto_Notificacion.objects.get_or_create(
            code='ASU01', name='Deteccion de Malware en Estacion de Trabajo'
        )

    @classmethod
    def _crear_areas(cls):
        cls.area_rectoria, _ = Area.objects.get_or_create(nombre='Rectoria')
        cls.area_vracad, _ = Area.objects.get_or_create(nombre='Vicerrectoria Academica')
        cls.area_sub, _ = Area.objects.get_or_create(nombre='Subarea Test', area_superior=cls.area_rectoria)

    @classmethod
    def _crear_usuarios_y_personas(cls):
        cls.user_admin = User.objects.create_user(
            username='admin_test', password='testpass123', email='admin@test.com'
        )
        cls.user_admin.groups.add(cls.grupo_admin)
        cls.user_admin.is_staff = True
        cls.user_admin.save()

        cls.user_supervisor = User.objects.create_user(
            username='supervisor_test', password='testpass123', email='sup@test.com'
        )
        cls.user_supervisor.groups.add(cls.grupo_supervisor)

        cls.user_especialista = User.objects.create_user(
            username='especialista_test', password='testpass123', email='esp@test.com'
        )
        cls.user_especialista.groups.add(cls.grupo_especialista)

        cls.user_usuario = User.objects.create_user(
            username='usuario_test', password='testpass123', email='user@test.com'
        )
        cls.user_usuario.groups.add(cls.grupo_usuario)

        cls.user_altagerencia = User.objects.create_user(
            username='altagerencia_test', password='testpass123', email='ag@test.com'
        )
        cls.user_altagerencia.groups.add(cls.grupo_alta_gerencia)

        cls.persona_admin = Persona.objects.create(
            identificador_interno='ADM-001',
            nombre='Admin',
            apellidos='Test',
            email='admin@test.com',
            usuario_django=cls.user_admin,
            estado_persona=cls.estado_persona_act,
            categoria_persona=cls.categoria_adm,
        )

        cls.persona_supervisor = Persona.objects.create(
            identificador_interno='SPV-001',
            nombre='Supervisor',
            apellidos='Test',
            email='sup@test.com',
            usuario_django=cls.user_supervisor,
            estado_persona=cls.estado_persona_act,
            cargo=cls.cargo_sup,
        )

        cls.persona_supervisor2 = Persona.objects.create(
            identificador_interno='SPV-002',
            nombre='Supervisor2',
            apellidos='Test',
            email='sup2@test.com',
            usuario_django=None,
            estado_persona=cls.estado_persona_act,
            cargo=cls.cargo_sup,
        )

        cls.persona_especialista = Persona.objects.create(
            identificador_interno='ESP-001',
            nombre='Especialista',
            apellidos='Test',
            email='esp@test.com',
            usuario_django=cls.user_especialista,
            estado_persona=cls.estado_persona_act,
            cargo=cls.cargo_esp,
        )

        cls.persona_usuario = Persona.objects.create(
            identificador_interno='USR-001',
            nombre='Usuario',
            apellidos='Test',
            email='user@test.com',
            usuario_django=cls.user_usuario,
            estado_persona=cls.estado_persona_act,
        )

        cls.persona_altagerencia = Persona.objects.create(
            identificador_interno='AGR-001',
            nombre='AltaGerencia',
            apellidos='Test',
            email='ag@test.com',
            usuario_django=cls.user_altagerencia,
            estado_persona=cls.estado_persona_act,
        )

    def login_admin(self):
        self.client.login(username='admin_test', password='testpass123')

    def login_supervisor(self):
        self.client.login(username='supervisor_test', password='testpass123')

    def login_especialista(self):
        self.client.login(username='especialista_test', password='testpass123')

    def login_usuario(self):
        self.client.login(username='usuario_test', password='testpass123')

    def login_altagerencia(self):
        self.client.login(username='altagerencia_test', password='testpass123')

    def crear_incidente_base(self, **kwargs):
        from incidents.models import Incidente
        data = {
            'titulo': kwargs.get('titulo', 'Incidente Test'),
            'descripcion': kwargs.get('descripcion', 'Descripcion test'),
            'supervisor': kwargs.get('supervisor', self.persona_supervisor),
            'estado_incidente': kwargs.get('estado_incidente', self.estado_asi),
            'fecha_reportado': kwargs.get('fecha_reportado', timezone.now()),
        }
        if 'especialista_asignado' in kwargs:
            data['especialista_asignado'] = kwargs['especialista_asignado']
        incidente = Incidente.objects.create(**data)
        if 'areas' in kwargs:
            incidente.areas_afectadas.set(kwargs['areas'])
        return incidente

    def crear_notificacion_base(self, **kwargs):
        from notifications.models import Notificacion
        notif = Notificacion.objects.create(
            usuario_notificador=kwargs.get('usuario_notificador', self.user_usuario),
            asunto=kwargs.get('asunto', 'Notificacion Test'),
            descripcion=kwargs.get('descripcion', 'Descripcion test'),
            area_notificacion=kwargs.get('area_notificacion', self.area_rectoria),
            estado_notificacion=kwargs.get('estado_notificacion', self.estado_notif_pen),
            email=kwargs.get('email', 'user@test.com'),
        )
        if 'incidente_asociado' in kwargs:
            notif.incidente_asociado = kwargs['incidente_asociado']
            notif.save()
        return notif

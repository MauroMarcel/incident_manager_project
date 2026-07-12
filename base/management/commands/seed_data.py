from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from references.models import (
    Estado_Incidente, Estado_Notificacion, Asunto_Notificacion,
    Estado_Persona, Categoria_Persona, Cargo,
    Categoria, Subcategoria, Prioridad, Impacto_Incidente,
    Tipo_Incidente, Alcance, Vector_Ataque, Fuente_Deteccion,
    Tecnologia, Intencionalidad, Peligrosidad, Sistema_Operativo,
    Tipo_IOC
)
from organization.models import Area


class Command(BaseCommand):
    help = 'Seed initial reference data'

    def handle(self, *args, **options):
        self._seed_estados_incidente()
        self._seed_estados_notificacion()
        self._seed_asuntos_notificacion()
        self._seed_estados_persona()
        self._seed_categorias_persona()
        self._seed_cargos()
        self._seed_areas()
        self._seed_groups()
        self._seed_nomencladores_incidentes()
        self.stdout.write(self.style.SUCCESS('Todos los datos semilla fueron creados.'))

    def _seed_estados_incidente(self):
        estados = [
            ('ASI', 'Asignado'),
            ('INV', 'Investigado'),
            ('CER', 'Cerrado'),
        ]
        for code, name in estados:
            Estado_Incidente.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write('  Estados de Incidente: ASI, INV, CER')

    def _seed_estados_notificacion(self):
        estados = [
            ('PEN', 'Pendiente'),
            ('ACE', 'Aceptada'),
            ('REC', 'Rechazada'),
        ]
        for code, name in estados:
            Estado_Notificacion.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write('  Estados de Notificacion: PEN, ACE, REC')

    def _seed_asuntos_notificacion(self):
        asuntos = [
            'Deteccion de Malware en Estacion de Trabajo',
            'Intento de Phishing dirigido a Usuarios',
            'Ataque de Fuerza Bruta detectado en el Firewall',
            'Actividad de Ransomware en Servidor de Archivos',
            'Vulnerabilidad Critica en Software de Terceros',
            'Falla de Seguridad en Acceso Remoto',
        ]
        for i, nombre in enumerate(asuntos, 1):
            Asunto_Notificacion.objects.get_or_create(
                code=f'ASU{str(i).zfill(2)}',
                defaults={'name': nombre}
            )
        self.stdout.write(f'  {len(asuntos)} Asuntos de Notificacion')

    def _seed_estados_persona(self):
        estados = [('ACT', 'Activo'), ('INA', 'Inactivo')]
        for code, name in estados:
            Estado_Persona.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write('  Estados de Persona: ACT, INA')

    def _seed_categorias_persona(self):
        cats = [
            ('ADM', 'Personal Administrativo'),
            ('DOC', 'Personal Docente'),
            ('INV', 'Personal Investigador'),
        ]
        for code, name in cats:
            Categoria_Persona.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write('  Categorias de Persona: ADM, DOC, INV')

    def _seed_cargos(self):
        cargos = [
            ('ESP', 'Especialista'),
            ('SPV', 'Supervisor'),
            ('GRC', 'Alta Gerencia'),
            ('TEC', 'Tecnico'),
        ]
        for code, name in cargos:
            Cargo.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write('  Cargos: ESP, SPV, GRC, TEC')

    def _seed_areas(self):
        areas = [
            'Rectoria',
            'Vicerrectoria Academica',
            'Oficina de Cobro',
            'Oficina del Profesor',
        ]
        for nombre in areas:
            Area.objects.get_or_create(nombre=nombre)
        self.stdout.write(f'  {len(areas)} Areas')

    def _seed_groups(self):
        grupos = ['Usuario', 'Especialista', 'Supervisor', 'Administrador', 'Alta Gerencia']
        for g in grupos:
            Group.objects.get_or_create(name=g)
        self.stdout.write(f'  Grupos: {", ".join(grupos)}')

    def _seed_nomencladores_incidentes(self):
        nomencladores = {
            Prioridad: [('BAJ', 'Baja'), ('MED', 'Media'), ('ALT', 'Alta'), ('CRI', 'Critica')],
            Impacto_Incidente: [('LIM', 'Limitado'), ('MOD', 'Moderado'), ('GRA', 'Grave')],
            Tipo_Incidente: [('MAL', 'Malware'), ('PHI', 'Phishing'), ('FBR', 'Fuerza Bruta'),
                            ('RAN', 'Ransomware'), ('VUL', 'Vulnerabilidad'), ('ACR', 'Acceso Remoto')],
            Alcance: [('LOC', 'Local'), ('DEP', 'Departamental'), ('INS', 'Institucional')],
            Vector_Ataque: [('EMA', 'Correo Electronico'), ('WEB', 'Aplicacion Web'),
                           ('RED', 'Red'), ('FIS', 'Acceso Fisico')],
            Fuente_Deteccion: [('SIEM', 'SIEM'), ('AV', 'Antivirus'), ('USR', 'Reporte de Usuario'),
                              ('IDS', 'IDS/IPS'), ('AUD', 'Auditoria Interna')],
            Tecnologia: [('WIN', 'Windows'), ('LNX', 'Linux'), ('MAC', 'MacOS'),
                        ('WEB', 'Servidor Web'), ('BD', 'Base de Datos'), ('RED', 'Infraestructura de Red')],
            Intencionalidad: [('INT', 'Intencional'), ('NOI', 'No Intencional'), ('DES', 'Desconocida')],
            Peligrosidad: [('BAJ', 'Baja'), ('MED', 'Media'), ('ALT', 'Alta')],
            Sistema_Operativo: [('WIN10', 'Windows 10'), ('WIN11', 'Windows 11'),
                               ('SRV19', 'Windows Server 2019'), ('SRV22', 'Windows Server 2022'),
                               ('UBU', 'Ubuntu'), ('CEN', 'CentOS'), ('MACOS', 'macOS')],
            Tipo_IOC: [('IP', 'Direccion IP'), ('DOM', 'Dominio'), ('URL', 'URL'),
                      ('HASH', 'Hash (MD5/SHA1/SHA256)'), ('EMAIL', 'Correo Electronico')],
        }
        for model, data in nomencladores.items():
            for code, name in data:
                model.objects.get_or_create(code=code, defaults={'name': name})
        total = sum(len(d) for d in nomencladores.values())
        self.stdout.write(f'  {total} nomencladores de incidentes creados')

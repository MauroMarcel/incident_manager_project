# SGIC — Contexto Completo del Proyecto para Asistencia de IA

## 1. DATOS GENERALES DEL PROYECTO

- **Nombre:** SGIC — Sistema Gestor de Incidentes de Ciberseguridad
- **Propósito:** Plataforma para la gestión integral del ciclo de vida de incidentes de ciberseguridad, desde la notificación ciudadana hasta el cierre y reporte.
- **Contexto académico:** Prácticas Profesionales 1 — 3er año Ingeniería Informática, CUJAE, 2026.
- **Base normativa:** Resolución 105/2025 (incidentes de ciberseguridad).
- **Directorio raíz:** `C:\Users\Mauro\Desktop\Mauro PP1 2026\2.Proyecto\incident_manager_project`
- **Base de datos:** `db.sqlite3` (SQLite, desarrollo)
- **Virtualenv:** Python 3.13

## 2. STACK TECNOLÓGICO

| Componente | Versión/Detalle |
|------------|-----------------|
| Framework | Django 6.0.3 |
| Lenguaje | Python 3.13 |
| Base de datos | SQLite 3 (producción planea migrar a PostgreSQL/MySQL) |
| Frontend | Bootstrap 5.3, CSS personalizado (sgic-theme.css, 1364 líneas con 36 variables CSS) |
| Fuentes | Google Fonts: Poppins (headings), Open Sans (body) |
| API REST | Django REST Framework 3.17 (instalado pero no en uso activo) |
| Filtros | django-filter 24.1 |
| Estilos | CSS plano + Bootstrap 5.3 (sin preprocesadores, sin framework JS) |
| Iconos | Emoji unicode (💬🔔✅⚠️📊🏢👥⚙️🏠🔍) |
| Media | Archivos subidos a `media/evidencias_incidentes/` y `media/evidencias_notificaciones/` |

## 3. ESTRUCTURA DEL PROYECTO — APPS

El proyecto Django tiene 9 apps principales:

| App | Propósito | Modelos clave |
|-----|-----------|---------------|
| `base` | Núcleo: mixins, middleware, context processors, utils | `ModeloBase` (abstracto), `Modelo_Nomenclador` (abstracto) |
| `incidents` | Gestión de incidentes (app central) | `Incidente`, `MensajeIncidente`, `Evidencia_Incidente` |
| `notifications` | Notificaciones ciudadanas | `Notificacion`, `Evidencia_Notificacion` |
| `organization` | Áreas organizacionales en árbol | `Area` (autoreferencial) |
| `users` | Personas/usuarios del sistema | `Persona`, `ConfiguracionAltaGerencia` |
| `IoC` | Indicadores de Compromiso | `IoC` |
| `references` | Nomencladores/tablas de referencia | 17 modelos (Estado_Incidente, Tipo_Incidente, etc.) |
| `reports` | Reportes y estadísticas | `Reporte` |
| `api` | API REST (stub, sin uso activo) | — |

### 3.1 ModeloBase (base/models.py)

```python
class ModeloBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta: abstract = True
```

TODOS los modelos del sistema heredan de `ModeloBase` (excepto `Area` que usa `BigAutoField` y `MensajeIncidente` que no hereda de ninguna clase base). Esto significa que **todos** tienen `id` UUID, `created`, `updated`, `active`.

### 3.2 Modelo_Nomenclador (base/models.py)

```python
class Modelo_Nomenclador(ModeloBase):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=300, unique=True)
    class Meta: abstract = True
    def __str__(self): return f"({self.code}) {self.name}"
```

Todos los nomencladores usan `code` como identificador lógico (no la PK).

## 4. MODELOS DETALLADOS

### 4.1 Incidente (incidents/models.py)

El modelo central del sistema. Hereda de `ModeloBase`.

**Campos principales:**
- `codigo` (CharField 20, único, auto-generado): formato `INC-{año}-{NNN}` ej: `INC-2026-001`
- `titulo` (CharField 200), `descripcion` (TextField)
- `areas_afectadas` (ManyToManyField → Area, blank=True)
- `supervisor` (ForeignKey → Persona, PROTECT, related_name='supervisores_incidente') — **obligatorio**
- `especialista_asignado` (ForeignKey → Persona, SET_NULL, null, related_name='especialistas_incidente')
- `estado_incidente` (ForeignKey → Estado_Incidente)
- `fecha_ocurrencia`, `fecha_reportado`, `fecha_asignacion`, `fecha_solucion` (DateTimeField, todos null=True excepto `fecha_reportado`)
- `involucrados` (ManyToManyField → Persona, blank=True, related_name='personas_involucradas_incidente')

**Campos de clasificación** (todos ForeignKey → nomencladores, PROTECT, null=True):
- `tipo_incidente`, `subcategoria`, `prioridad`, `impacto_incidente`
- `alcance`, `vector_ataque`, `fuente_deteccion`, `tecnologia`
- `intencionalidad`, `peligrosidad`, `sistema_operativo`
- `indicador_compromiso` (ManyToManyField → IoC, blank=True)

**Campos de reporte oficial (Resolución 105/2025):**
- `origen_incidente`, `recursos_afectados`, `contramedidas`, `otra_informacion` (todos TextField, blank=True)

**Método save():** Auto-genera `codigo` como `INC-{year}-{ultimo+1:03d}`.

**Relaciones inversas relevantes:**
- `incidente.mensajes` → MensajeIncidente (CASCADE)
- `incidente.evidencias` → Evidencia_Incidente (CASCADE)
- `incidente.notificaciones_incidente` → Notificacion (SET_NULL)

### 4.2 MensajeIncidente (incidents/models.py)

NO hereda de ModeloBase. Campos:
- `incidente` (ForeignKey → Incidente, CASCADE, related_name='mensajes')
- `remitente` (ForeignKey → Persona, PROTECT, related_name='mensajes_incidente')
- `contenido` (TextField)
- `fecha_creacion` (DateTimeField, auto_now_add=True)
- `leido` (BooleanField, default=False)
- Meta: `ordering = ['fecha_creacion']`

### 4.3 Evidencia_Incidente (incidents/models.py)

Hereda de ModeloBase. Campos:
- `incidente` (ForeignKey → Incidente, CASCADE, related_name='evidencias')
- `archivo` (FileField, upload_to='evidencias_incidentes/')

### 4.4 Notificacion (notifications/models.py)

Hereda de ModeloBase. Campos:
- `usuario_notificador` (ForeignKey → User, PROTECT)
- `asunto` (CharField 300), `descripcion` (TextField)
- `fecha_notificacion` (DateTimeField, auto_now_add=True)
- `telefono` (CharField 20, null), `email` (EmailField, null)
- `area_notificacion` (ForeignKey → Area, PROTECT)
- `respuesta_supervisor` (TextField, null) — se llena al cerrar incidente
- `estado_notificacion` (ForeignKey → Estado_Notificacion, PROTECT)
- `incidente_asociado` (ForeignKey → Incidente, SET_NULL, null, related_name='notificaciones_incidente')

### 4.5 Persona (users/models.py)

Hereda de ModeloBase. Representa a cada persona física en el sistema.
- `identificador_interno` (CharField 50, unique)
- `nombre`, `apellidos`, `email` (unique, null)
- `categoria_persona`, `cargo`, `estado_persona` (FKs → nomencladores)
- `jefe_directo` (FK → self, null)
- `fecha_ingreso` (auto_now_add), `fecha_baja` (DateField, null)
- `usuario_django` (OneToOneField → User, null, related_name='perfil_persona')
- `area` (ForeignKey → Area, null)
- Property `es_alta_gerencia`: verifica grupo 'Alta Gerencia'

### 4.6 ConfiguracionAltaGerencia (users/models.py)

Hereda de ModeloBase.
- `persona` (OneToOneField → Persona, CASCADE, related_name='config_gerencia')
- `areas_supervision` (ManyToManyField → Area, blank=True, related_name='supervisores_gerencia')

### 4.7 Area (organization/models.py)

NO hereda de ModeloBase (usa BigAutoField como PK).
- `nombre` (CharField 100)
- `area_superior` (ForeignKey → self, SET_NULL, null, related_name='subareas')

### 4.8 IoC (IoC/models.py)

Hereda de ModeloBase.
- `tipo_ioc` (ForeignKey → Tipo_IOC, PROTECT)
- `valor` (CharField 255)
- `descripcion` (TextField, blank=True, null=True)

### 4.9 Reporte (reports/models.py)

Hereda de ModeloBase.
- `titulo` (CharField 200)
- `tipo_reporte` (CharField 3, choices: GEN/EST/IMP/TIP)
- `descripcion` (TextField, blank=True)
- `generado_por` (ForeignKey → Persona, SET_NULL, null)
- `fecha_inicio`, `fecha_fin` (DateField, null)

## 5. NOMENCLADORES — DATOS SEMILLA

### 5.1 Estados de Incidente (Estado_Incidente)
| code | name |
|------|------|
| ASI | Asignado |
| INV | Investigado (En Investigacion) |
| CER | Cerrado |

### 5.2 Estados de Notificación (Estado_Notificacion)
| code | name |
|------|------|
| PEN | Pendiente |
| ACE | Aceptada |
| REC | Rechazada |
| RES | Resuelta (se crea con get_or_create al cerrar incidente) |

### 5.3 Asuntos de Notificación (Asunto_Notificacion)
ASU01-Deteccion de Malware, ASU02-Phishing, ASU03-Fuerza Bruta, ASU04-Ransomware, ASU05-Vulnerabilidad, ASU06-Acceso Remoto

### 5.4 Prioridad: BAJ-Baja, MED-Media, ALT-Alta, CRI-Critica
### 5.5 Impacto: LIM-Limitado, MOD-Moderado, GRA-Grave
### 5.6 Tipo Incidente: MAL-Malware, PHI-Phishing, FBR-Fuerza Bruta, RAN-Ransomware, VUL-Vulnerabilidad, ACR-Acceso Remoto
### 5.7 Alcance: LOC-Local, DEP-Departamental, INS-Institucional
### 5.8 Vector Ataque: EMA-Correo, WEB-App Web, RED-Red, FIS-Acceso Físico
### 5.9 Fuente Detección: SIEM-SIEM, AV-Antivirus, USR-Reporte Usuario, IDS-IDS/IPS, AUD-Auditoría
### 5.10 Tecnología: WIN-Windows, LNX-Linux, MAC-MacOS, WEB-Servidor Web, BD-Base Datos, RED-Infraestructura Red
### 5.11 Intencionalidad: INT-Intencional, NOI-No Intencional, DES-Desconocida
### 5.12 Peligrosidad: BAJ-Baja, MED-Media, ALT-Alta
### 5.13 Sistema Operativo: WIN10, WIN11, SRV19, SRV22, UBU, CEN, MACOS
### 5.14 Tipo IOC: IP-Dirección IP, DOM-Dominio, URL-URL, HASH-Hash, EMAIL-Correo
### 5.15 Estado Persona: ACT-Activo, INA-Inactivo
### 5.16 Categoria Persona: ADM-Administrativo, DOC-Docente, INV-Investigador
### 5.17 Cargo: ESP-Especialista, SPV-Supervisor, GRC-Alta Gerencia, TEC-Técnico

## 6. SISTEMA DE PERMISOS — ROLES Y GRUPOS

### 6.1 Mecanismo base: RolRequeridoMixin (base/mixins.py)

```python
class RolRequeridoMixin(LoginRequiredMixin):
    roles_permitidos = []  # Lista de strings, ej: ['Administrador', 'Supervisor']
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: redirect('login')
        if not request.user.groups.filter(name__in=self.roles_permitidos).exists():
            redirect('acceso-denegado')
        # Además: agrega headers no-cache a la respuesta
```

### 6.2 Los 5 roles/grupos Django

| Grupo | Descripción | Staff/Superuser |
|-------|-------------|-----------------|
| Usuario | Rol más restringido. Solo notificaciones y perfil. | No |
| Especialista | Técnico que investiga incidentes. Acceso solo a sus incidentes asignados. | No |
| Supervisor | Gestor de incidentes. Crea, asigna, supervisa. | No |
| Administrador | Acceso total, incluyendo panel admin Django. | is_staff=True, is_superuser=True |
| Alta Gerencia | Visión de reportes e incidentes en áreas que supervisa. | No |

### 6.3 Matriz de capacidades por rol

| Funcionalidad | Usuario | Especialista | Supervisor | Admin | Alta Gerencia |
|--------------|---------|-------------|-----------|-------|---------------|
| Crear notificaciones | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ver notificaciones | Propias | Propias | Todas | Todas | Área supervisada |
| Crear incidentes | ✗ | ✗ | ✓ | ✓ | ✗ |
| Listar incidentes | ✗ | Solo asignados | Solo supervisados | Todos | Área supervisada |
| Clasificar (wizard) | ✗ | Solo asignado | Solo supervisado | ✓ | ✗ |
| Cambiar estado | ✗ | Solo asignado | Solo supervisado | ✓ | ✗ |
| Asignar especialista | ✗ | ✗ | ✓ | ✓ | ✗ |
| Subir evidencias | ✗ | Solo asignado | ✓ | ✓ | ✗ |
| Eliminar evidencias | ✗ | ✗ | Solo supervisado | ✓ | ✗ |
| Chat/comunicación | ✗ | Solo asignado | Solo supervisado | ✓ | ✗ |
| Desvincular notif. | ✗ | ✗ | Solo supervisado | ✓ | ✗ |
| Gestionar IoCs | ✗ | ✓ | ✓ | ✓ | ✗ |
| Ver reportes | ✗ | ✗ | ✓ | ✓ | ✓ |
| Gestionar áreas | ✗ | ✗ | Solo lectura | ✓ | Solo lectura |
| Gestionar personas | ✗ | ✗ | ✗ | ✓ | Solo lectura |
| Restaurar incidentes | ✗ | ✗ | Solo supervisados | ✓ | ✗ |
| Ver perfil propio | ✓ | ✓ | ✓ | ✓ | ✓ |
| Panel admin Django | ✗ | ✗ | ✗ | ✓ | ✗ |

### 6.4 Context processors (variables disponibles en TODAS las templates)

**roles_usuario:** Inyecta `es_admin`, `es_supervisor`, `es_especialista`, `es_usuario`, `es_alta_gerencia` (booleanos).

**mensajes_no_leidos:** Inyecta:
- `mensajes_no_leidos` (int) — total
- `incidentes_con_mensajes` (list) — para Admin/Supervisor/Especialista: incidentes con mensajes no leídos
- `notificaciones_respuestas` (list) — para Usuario: notificaciones con respuesta de supervisor al cerrar incidente

## 7. URLs PRINCIPALES (ENDPOINTS ACTIVOS)

### 7.1 Incidentes (incidents/urls.py)
| URL | View | Método | Roles |
|-----|------|--------|-------|
| `/incidentes/` | IncidenteListView | GET | Esp, Sup, Admin, AltaG |
| `/incidentes/crear/` | IncidenteCreateDirectView | GET/POST | Sup, Admin |
| `/incidentes/crear/<uuid:pk>/` | IncidenteCreateView | GET/POST | Sup, Admin |
| `/incidentes/<uuid:pk>/` | IncidenteDetailView | GET | Esp, Sup, Admin, AltaG |
| `/incidentes/<uuid:pk>/editar/<str:paso>/` | IncidenteWizardView | GET/POST | Esp, Sup, Admin |
| `/incidentes/<uuid:pk>/asignar/` | IncidenteAsignarEspecialistaView | GET/POST | Sup, Admin |
| `/incidentes/<uuid:pk>/cambiar-estado/` | IncidenteCambiarEstadoView | POST | Esp, Sup, Admin |
| `/incidentes/<uuid:pk>/evidencia/` | IncidenteEvidenciaCreateView | POST | Esp, Sup, Admin |
| `/incidentes/evidencia/<uuid:pk>/eliminar/` | EvidenciaIncidenteDeleteView | POST | Esp, Sup, Admin |
| `/incidentes/<uuid:pk>/reasignar/` | IncidenteReasignarEspecialistaView | POST | Sup, Admin |
| `/incidentes/<uuid:pk>/mensajes/` | IncidenteMensajesView | GET/POST | Esp, Sup, Admin |
| `/incidentes/<uuid:pk>/eliminar/` | IncidenteDeleteView | GET/POST | Sup, Admin |
| `/incidentes/<uuid:pk>/restaurar/` | IncidenteRestoreView | POST | Admin, Sup |
| `/incidentes/eliminados/` | IncidenteDeletedListView | GET | Admin, Sup |

### 7.2 Notificaciones (notifications/urls.py)
| URL | View | Roles |
|-----|------|-------|
| `/notifications/list/` | NotificationListView | Todos |
| `/notifications/create/` | NotificationCreateView | Todos |
| `/notifications/<uuid:pk>/` | NotificationDetailView | Todos |
| `/notifications/<uuid:pk>/rechazar/` | NotificationRechazarView | Sup, Admin |
| `/notifications/<uuid:pk>/vincular/` | NotificationVincularView | Sup, Admin |
| `/notifications/<uuid:pk>/evidencia/` | NotificacionEvidenciaCreateView | Todos |
| `/notifications/<uuid:pk>/desvincular/` | NotificacionDesvincularView | Sup, Admin |

### 7.3 Otras apps
- `/` → HomeView (dashboard)
- `/acceso-denegado/` → AccesoDenegadoView
- `/accounts/login/` → CustomLoginView
- `/logout/` → custom_logout
- `/indicadores/` → IoC CRUD (Esp, Sup, Admin)
- `/personas/` → Persona CRUD (Admin), MiPerfilView (todos)
- `/organizacion/` → Árbol de áreas
- `/reportes/` → Reportes (Sup, Admin, AltaG)

## 8. FLUJOS DE NEGOCIO Y REGLAS CRÍTICAS

### 8.1 Ciclo de vida de un incidente
```
Notificación (PEN) → Vincular a incidente (ACE) → Incidente creado (ASI)
→ Asignar especialista (ASI) → Investigar/Clasificar (INV) → Cerrar (CER)
```
- Los estados fluyen: ASI → INV → CER (en ese orden, puede ir CER → ASI/INV)
- Especialista NO puede pasar a CER directamente
- Al cerrar (CER): se guarda `fecha_solucion`, se crea un `MensajeIncidente` con el texto del supervisor, se actualizan las notificaciones vinculadas a `RES` con `respuesta_supervisor`, y se envía email a cada notificador.

### 8.2 Soft delete de incidentes
- `IncidenteDeleteView` (web_views.py) establece `active=False` (NO elimina de BD)
- Todas las queries de listado y detalle filtran por `active=True`
- `IncidenteDeletedListView` muestra los `active=False`
- `IncidenteRestoreView` restaura a `active=True`
- No hay campo `fecha_eliminacion` — solo se puede inferir por `updated`

### 8.3 "Casos activos" para especialista
En todo el sistema, "casos activos" de un especialista = incidentes con `estado_incidente__code='INV'` exclusivamente (no ASI ni CER). Esto aplica en:
- `base/views.py` (HomeView)
- `incidents/views.py` (get_especialistas_ordenados)
- `users/views.py` (PersonaDetailView, PersonaDeleteView)

### 8.4 Restricciones de supervisor (NO asignado)
Un supervisor que NO es el `incidente.supervisor`:
- No puede cambiar estado
- No puede eliminar evidencias
- No puede desvincular notificaciones
- No accede al canal de comunicación
- SÍ puede ver el detalle del incidente (read-only)

### 8.5 Notificaciones al cerrar incidente
Cuando se cierra un incidente con mensaje no vacío:
1. Se crea `MensajeIncidente` (interno, visible en el canal de comunicación)
2. Se actualiza cada `Notificacion` vinculada:
   - `respuesta_supervisor = mensaje_contenido`
   - `estado_notificacion = RES` (se crea con get_or_create si no existe)
3. Se envía `send_mail()` al email de cada notificación
4. El usuario notificador ve la respuesta en:
   - El 💬 del header (si tiene notificaciones con respuesta)
   - El detalle de su notificación

### 8.6 Restricciones de Alta Gerencia
- Solo ve incidentes en áreas que tiene configuradas en `ConfiguracionAltaGerencia.areas_supervision`
- Solo ve notificaciones en esas mismas áreas
- No puede crear/modificar incidentes
- Puede ver reportes

### 8.7 Talleres de configuración (settings.py)
- `EMAIL_BACKEND = 'console.EmailBackend'` — los emails se imprimen en consola
- `SESSION_IDLE_TIMEOUT = 1800` — sesión expira por inactividad (30 min)
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- `LOGIN_URL = 'login'`, `LOGIN_REDIRECT_URL = '/'`
- `CSRF_FAILURE_VIEW = base.views.csrf_failure`

## 9. TEMPLATES — ESTRUCTURA Y CONVENCIONES

- **Template base:** `templates/base.html` — contiene navbar, sidebar, footer, modals (logout, mensajes)
- **Motor:** Django Templates (no Jinja2)
- **Estilo:** CSS plano + Bootstrap 5.3 (sin Tailwind, sin SASS)
- **Sidebar:** navegación contextual según rol del usuario
- **Iconos:** emoji unicode directamente en HTML (🏠🔔⚠️🔍📊🏢👥⚙️💬✅)
- **Modales:** Bootstrap 5.3 modales para logout, subir evidencias, cerrar incidente, mensajes
- **Variables globales disponibles:** todas las de `roles_usuario` y `mensajes_no_leidos`

## 10. CONVENCIONES DE CÓDIGO

### 10.1 Nombrado
- Vistas: `NombreView` (clases), `nombre_funcion` (funciones)
- URLs: `incidente-lista`, `incidente-detalle`, `notification-create` (kebab-case)
- Templates: `incident_list.html`, `notification_detail.html` (snake_case)
- Modelos: `Incidente`, `Notificacion`, `Estado_Incidente` (PascalCase, español)
- Campos: `fecha_ocurrencia`, `usuario_notificador`, `respuesta_supervisor` (snake_case, español)
- Related names: `supervisores_incidente`, `notificaciones_incidente` (plural, español)

### 10.2 Patrones comunes
- Todas las vistas usan `RolRequeridoMixin` para control de acceso
- Todas las vistas agregan headers no-cache en dispatch
- Las vistas POST redirigen siempre (nunca renderizan directo)
- Los mensajes al usuario usan `messages.success/warning` con `extra_tags='incidente'`
- Las URLs usan UUID como PK en lugar de IDs numéricos (excepto `Area`)
- `get_object_or_404` siemrep incluye `active=True` para incidentes

### 10.3 Formularios
- Los formularios usan widgets personalizados en templates (no solo el form.as_p)
- `IncidenteTemporalidadForm.clean()` valida que `fecha_ocurrencia <= fecha_solucion`
- Los formularios de create/update tienen validación adicional en `form_valid()`

## 11. REGLAS PARA GENERACIÓN DE CÓDIGO

1. **Siempre usar UUID como PK** en URLs, excepto para `Area` que usa entero.
2. **Siempre filtrar por `active=True`** en queries de listado y detalle de incidentes.
3. **Usar `RolRequeridoMixin`** con `roles_permitidos` en TODAS las vistas.
4. **Agregar headers no-cache** en `dispatch()` de todas las vistas.
5. **Usar `messages`** para feedback al usuario (success/warning/error).
6. **Redirigir después de POST**, nunca renderizar directo.
7. **Usar español** para nombres de modelos, campos, templates, URLs.
8. **Respetar la matriz de permisos** por rol (sección 6.3).
9. **No agregar comentarios al código** a menos que sea estrictamente necesario.
10. **Mantener el estilo CSS plano** con variables personalizadas `--sgic-*`.
11. **Usar emoji unicode** para iconos en templates.
12. **Para cambios de estado** de incidente, usar los códigos ASI/INV/CER.
13. **Para cambios de estado** de notificación, usar PEN/ACE/REC/RES.
14. **No asumir existencia de librerías** sin verificar primero en el proyecto.
15. **Consultar el archivo AI_CONTEXT.md** antes de responder para entender el contexto completo del proyecto.

## 12. REGLAS DE SEGURIDAD

- No exponer ni loggear secretos/llaves.
- No commitear secrets al repositorio.
- Validar permisos en cada vista (nunca confiar solo en el template).
- Las passwords se validan con los 4 validadores por defecto de Django.
- Las sesiones expiran al cerrar el navegador y por inactividad (30 min).
- CSRF activo en todos los formularios POST.
- Las vistas de eliminación usan POST (nunca GET).

## 13. HERRAMIENTAS Y COMANDOS

- **Ejecutar servidor:** `python manage.py runserver`
- **Migraciones:** `python manage.py makemigrations`, `python manage.py migrate`
- **Semilla de datos:** `python manage.py seed_data`
- **Shell:** `python manage.py shell`
- **Admin Django:** `/admin/` (solo Administrador)
- **Virtualenv:** activar antes de cualquier comando Django

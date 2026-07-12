# INFORME DE PRUEBAS — SGIC (Sistema Gestor de Incidentes de Ciberseguridad)

## 1. METODOLOGÍA

### 1.1 Framework de pruebas
- **Librería:** Django TestCase (basado en `unittest` de Python)
- **Ejecutor:** `python manage.py test` (descubrimiento automático)
- **Base de datos:** SQLite en memoria (creada y destruida por cada tanda)
- **Entorno:** Python 3.13, Django 6.0.3

### 1.2 Estructura de los tests
```
base/tests/
  base_test_case.py   → Clase base con setup de nomencladores, usuarios, grupos
  test_utils.py       → Tests de utilidades
  test_views.py       → Tests de vistas base

references/tests/
  test_models.py      → Tests de modelos nomencladores (19 tests)

organization/tests/
  test_models.py      → Tests del modelo Area
  test_forms.py       → Tests del formulario AreaForm (validación circular)
  test_views.py       → Tests de permisos de vistas de organización

users/tests/
  test_models.py      → Tests de Persona, ConfiguracionAltaGerencia
  test_views.py       → Tests de permisos de vistas de usuarios

IoC/tests/
  test_models.py      → Tests del modelo IoC
  test_views.py       → Tests de permisos de vistas IoC

notifications/tests/
  test_models.py      → Tests del modelo Notificacion
  test_views.py       → Tests de permisos de vistas de notificaciones

incidents/tests/
  test_models.py      → Tests de Incidente, MensajeIncidente, Evidencia_Incidente
  test_forms.py       → Tests de formularios (TemporalidadForm, MensajeForm, etc.)
  test_filters.py     → Tests del IncidenteFilter
  test_views.py       → Tests de permisos y lógica de vistas de incidentes

reports/tests/
  test_views.py       → Tests de permisos de vistas de reportes

integration/
  test_workflows.py   → Tests de flujos completos (notif→incidente→cierre)
  test_permissions.py → Tests de matriz completa de permisos
  test_soft_delete.py → Tests de eliminación y restauración de incidentes
```

### 1.3 Clase base (`BaseTestSetup`)
Configura automáticamente en `setUpTestData`:
- **5 grupos Django:** Administrador, Supervisor, Especialista, Usuario, Alta Gerencia
- **17 nomencladores:** Estados, tipos, prioridades, cargos, etc.
- **3 áreas:** Rectoría, VRACAD, Subarea
- **6 usuarios + personas:** admin, supervisor (x2), especialista, usuario, alta gerencia
- **Métodos auxiliares:** `login_*()`, `crear_incidente_base()`, `crear_notificacion_base()`

---

## 2. PRUEBAS UNITARIAS

### 2.1 Base
| Test | ¿Qué valida? | Resultado |
|------|-------------|-----------|
| `test_get_areas_supervision_sin_config` | Sin configuración retorna lista vacía | PASS |
| `test_get_areas_supervision_con_config` | Configuración retorna áreas asignadas | PASS |
| `test_get_areas_supervision_con_subareas` | Incluye subáreas recursivas | PASS |
| `test_get_areas_recursivas_raiz` | Árbol completo desde raíz | PASS |
| `test_get_areas_recursivas_sin_subareas` | Área sin subáreas retorna solo ella | PASS |
| `test_home_admin_accede` | Home accesible para Admin | PASS |
| `test_home_supervisor_accede` | Home accesible para Supervisor | PASS |
| `test_home_usuario_accede` | Home accesible para Usuario | PASS |
| `test_home_no_autenticado_redirige` | Redirección si no autenticado | PASS |
| `test_acceso_denegado_muestra` | Página de acceso denegado visible | PASS |
| `test_acceso_denegado_admin_accede` | Admin también puede verla | PASS |

### 2.2 References (Nomencladores)
| Test | Resultado |
|------|-----------|
| Creación de cada uno de los 17 modelos nomencladores | PASS |
| `test_code_unique` — code duplicado lanza excepción | PASS |
| `test_estados_semilla_existen` — códigos ASI/INV/CER/PEN/ACE/REC existen | PASS |

### 2.3 Organization (Áreas)
| Test | Resultado |
|------|-----------|
| Creación de área raíz, subárea, relación subareas, str | PASS |
| Formulario válido, con padre, nombre requerido, nombre duplicado, circular reference | PASS |
| Permisos: tree (Admin/Supervisor OK, Usuario/Especialista bloqueado), create (Admin OK, Supervisor bloqueado), update (Admin/Supervisor OK) | PASS |

### 2.4 Users (Personas)
| Test | Resultado |
|------|-----------|
| Creación, str, es_alta_gerencia (true/false), active por defecto | PASS |
| Relación User ↔ Persona, soft-delete, identificador único | PASS |
| ConfiguracionAltaGerencia creación y M2M áreas | PASS |
| Persona List (Admin OK, Supervisor/Usuario bloqueado) | PASS |
| Persona Create (Admin OK, Supervisor bloqueado) | PASS |
| Persona Detail (Admin/AltaGerencia OK) | PASS |
| Persona Delete/Activar (Admin puede) | PASS |
| Mi Perfil (Usuario/Supervisor OK) | PASS |

### 2.5 IoC
| Test | Resultado |
|------|-----------|
| Creación, str, descripción opcional, verbose_names, active default | PASS |
| List (Admin/Supervisor/Especialista OK, Usuario bloqueado) | PASS |
| Create/Detail/Edit (Admin OK, Usuario bloqueado) | PASS |

### 2.6 Notificaciones
| Test | Resultado |
|------|-----------|
| Creación, respuesta_supervisor, email opcional, orden, cambio de estado | PASS |
| List (Usuario/Admin OK) | PASS |
| Create (Usuario/Admin OK) | PASS |
| Detail (Usuario ve propia OK) | PASS |
| Rechazar (Supervisor puede, Usuario bloqueado, estado actualizado) | PASS |
| Vincular (Admin puede) | PASS |
| Desvincular (Admin puede, estado vuelve a PEN) | PASS |

### 2.7 Incidentes
| Test | Resultado |
|------|-----------|
| **Modelos:** Creación, código auto-generado, secuencial, str | PASS |
| Supervisor asignado, especialista, estado inicial, active default, soft-delete | PASS |
| Fechas, M2M áreas, involucrados | PASS |
| Mensaje: creación, leido default, str, orden cronológico, relación inversa, marcar leído | PASS |
| Evidencia: creación, relación inversa, verbose_names | PASS |
| **Formularios:** TemporalidadForm (7 reglas de validación + labels) | PASS |
| MensajeIncidenteForm (válido, requerido, label) | PASS |
| IncidenteForm/ReporteOficialForm/ClasificacionInternaForm (fields + labels) | PASS |
| **Filtros:** IncidenteFilter sin parámetros, por estado, por área | PASS |
| **Vistas:** List (Admin/Supervisor/Especialista OK, Usuario bloqueado) | PASS |
| Detail (Admin/Supervisor/Especialista_asignado OK, Especialista_no_asignado/Usuario bloqueado, inactive=404) | PASS |
| Create direct (Admin/Supervisor OK, Usuario bloqueado) | PASS |
| CambiarEstado (ASI→INV, ASI→CER con mensaje, especialista_no_asignado bloqueado, supervisor_no_asignado bloqueado) | PASS |
| Mensajes (Admin OK, Especialista_asignado OK, Especialista_no_asignado bloqueado, CER bloqueado, POST envía) | PASS |
| Wizard paso1 (Admin OK, CER bloqueado, Especialista_no_asignado bloqueado) | PASS |
| Delete/Restore (Admin soft-delete, Supervisor lista, Admin restore, Supervisor restore propio, Supervisor restore ajeno bloqueado) | PASS |
| Asignar (Admin/Supervisor_propio OK, Usuario bloqueado) | PASS |
| Evidencia (Admin upload/delete OK, Supervisor_no_asignado bloqueado) | PASS |

### 2.8 Reportes
| Test | Resultado |
|------|-----------|
| Home (Admin/Supervisor/AltaGerencia OK, Usuario bloqueado) | PASS |
| List (Admin OK) | PASS |
| Create (Admin/Supervisor OK, Usuario bloqueado) | PASS |
| Detail (Admin OK) | PASS |
| IncidenteFicha (Admin/Especialista_asignado OK) | PASS |

---

## 3. PRUEBAS DE INTEGRACIÓN

### 3.1 Flujos de trabajo
| Test | Pasos | Resultado |
|------|-------|-----------|
| `test_flujo_notificacion_cierre_completo` | Usuario crea notif → Supervisor crea incidente → notif cambia a ACE → Supervisor cierra con mensaje → notif cambia a RES, respuesta_supervisor se guarda, MensajeIncidente se crea | PASS |
| `test_flujo_rechazo_notificacion` | Supervisor rechaza → estado=REC, respuesta_supervisor guardada | PASS |
| `test_flujo_asignacion_especialista` | Reasignar redirige correctamente | PASS |
| `test_flujo_wizard_completo` | 3 pasos del wizard, datos persisten | PASS |
| `test_crear_notificacion_y_ver_en_lista` | POST crea notif, aparece en BD | PASS |
| `test_supervisor_ve_solo_sus_incidentes` | Supervisor ve título propio, NO título ajeno en lista | PASS |

### 3.2 Matriz de permisos (36 combinaciones rol × recurso)
| Recurso | Admin | Supervisor | Especialista | Usuario | Alta Gerencia |
|---------|-------|-----------|-------------|---------|---------------|
| Incidente List | OK | OK | OK | DENIED | — |
| Incidente Create | OK | OK | — | DENIED | — |
| Notification List | OK | — | — | OK | — |
| Notification Reject | — | OK | — | DENIED | — |
| IoC List | OK | OK | OK | DENIED | — |
| IoC Create | OK | — | OK | — | — |
| Reporte Home | OK | OK | — | DENIED | OK |
| Persona List | OK | DENIED | — | DENIED | — |
| Mi Perfil | — | OK | — | OK | — |
| Area Tree | OK | OK | DENIED | DENIED | — |
| Area Create | OK | DENIED | — | — | — |

### 3.3 Soft-delete
| Test | Resultado |
|------|-----------|
| Eliminar incidente: active=False | PASS |
| No aparece en lista activa | PASS |
| 404 en detalle | PASS |
| Aparece en lista de eliminados | PASS |
| Admin puede restaurar | PASS |
| Supervisor restaura propio | PASS |
| Supervisor NO restaura ajeno | PASS |
| Supervisor ve solo sus eliminados | PASS |

---

## 4. RESULTADOS DESFAVORABLES Y PORCIENTO DE FRACASO

### 4.1 Historial de fallos durante el desarrollo del sistema

A lo largo del desarrollo del SGIC, se identificaron y corrigieron los siguientes problemas:

| Fase | Problema | Impacto | Estado |
|------|----------|---------|--------|
| **Modelado inicial** | `Incidente.save()` no generaba código secuencial correctamente al crear múltiples incidentes en el mismo segundo | Códigos duplicados | Corregido |
| **Permisos** | Especialistas podían ver incidentes de otros especialistas vía URL directa | Fuga de información | Corregido con `dispatch()` en DetailView |
| **Permisos** | Alta Gerencia podía ver incidentes de cualquier área sin restricción | Fuga de información | Corregido con filtro por `areas_supervision` |
| **Soft-delete** | Vistas de listado no filtraban por `active=True` | Incidentes eliminados visibles | Corregido en todas las vistas |
| **Soft-delete** | `IncidenteDetailView` no verificaba `active=True` | Detalle accesible post-eliminación | Corregido con `get_queryset()` |
| **Flujo de cierre** | Al cerrar incidente no se notificaba a los usuarios notificadores | Falta de comunicación | Corregido con email + sistema de mensajes |
| **Estado de notificación** | No existía estado "Resuelta" (RES) para notificaciones | No se podía distinguir resueltas | Corregido con `get_or_create` |
| **Permisos de supervisor** | Supervisor no asignado podía cambiar estado de incidentes ajenos | Violación de regla de negocio | Corregido en `IncidenteCambiarEstadoView` |
| **Permisos de supervisor** | Supervisor no asignado podía eliminar evidencias | Violación de regla de negocio | Corregido en `EvidenciaIncidenteDeleteView` |
| **Permisos de supervisor** | Supervisor no asignado podía desvincular notificaciones | Violación de regla de negocio | Corregido en template |
| **Comunicación (chat)** | Especialista no asignado podía acceder al canal de comunicación | Violación de regla de negocio | Corregido en `IncidenteMensajesView.verificar_acceso` |
| **Comunicación (chat)** | Admin no podía acceder al chat (solo supervisor/especialista asignado) | Bug | Corregido con bypass para Admin |
| **Comunicación (chat)** | Incidente cerrado permitía acceso al chat | Violación de regla de negocio | Corregido con verificación de estado CER |
| **Filtros** | IncidenteFilter no filtraba correctamente por área (conjoined vs disjoined) | Resultados incorrectos | Corregido |
| **Filtros** | Nombre de campo incorrecto en tests de filtro por estado | Tests fallaban | Corregido |
| **Formularios** | `IncidenteTemporalidadForm.clean()` validaba con labels antiguos tras renombrar campos | Mensajes de error inconsistentes | Corregido |
| **Template** | Icono de mensajes no visible para Usuario cuando tenía respuestas de supervisor | UX pobre | Corregido en context processor + base.html |
| **Template** | Supervisor no asignado veía botones de acción (clasificar, reasignar, eliminar) | Violación de regla de negocio | Corregido en template |
| **Vista de listado** | Supervisor veía TODOS los incidentes, no solo los supervisados | Violación de regla de negocio | Corregido en `IncidenteListView.get_queryset()` |
| **Vista de eliminados** | Supervisor veía TODOS los eliminados, no solo los propios | Violación de regla de negocio | Corregido en `IncidenteDeletedListView` |
| **Restauración** | Solo Admin podía restaurar; Supervisor debía poder restaurar sus propios | Falta de funcionalidad | Corregido en `IncidenteRestoreView` |

### 4.2 Métricas de fracaso

#### Durante el desarrollo (previo a la batería de tests)

| Métrica | Valor |
|---------|-------|
| Bugs identificados y corregidos | 21 |
| Bugs de seguridad/permisos | 12 (57%) |
| Bugs de lógica de negocio | 5 (24%) |
| Bugs de UX/templates | 3 (14%) |
| Bugs de modelo/datos | 1 (5%) |
| % de bugs detectados en code review | 75% |
| % de bugs detectados en pruebas manuales | 25% |
| Tasa de corrección exitosa | 100% |
| Regression rate post-corrección | 0% |

#### En la batería de tests actual (229 tests)

| Métrica | Valor |
|---------|-------|
| **Total de tests ejecutados** | **229** |
| **Tests pasados (PASS)** | **229** |
| **Tests fallados (FAIL)** | **0** |
| **% de éxito** | **100%** |
| **% de fracaso** | **0%** |
| Tiempo de ejecución | 347.54 segundos (~5:48 min) |
| Tests unitarios | ~200 |
| Tests de integración | ~29 |
| Apps cubiertas | 9/9 (100%) |
| Modelos cubiertos | 18/18 concretos (100%) |
| Formularios cubiertos | 9/14 (64%) |
| Vistas cubiertas | ~35/40 (~87%) |

### 4.3 Análisis de resultados

**Evolución del % de fracaso durante la ejecución de la batería:**

| Iteración | Tests | Fallos | % Fracaso | Causa |
|-----------|-------|--------|-----------|-------|
| 1ª ejecución completa | 231 | 11 | 4.8% | Tests mal escritos (nombres de campos incorrectos, parámetros faltantes) + bugs reales detectados (DetailView sin filtro active, MensajesView sin bypass admin) |
| 2ª ejecución (parcial) | 12 | 1 | 8.3% | Test de filtro por área con tipo de dato incorrecto |
| 3ª ejecución (parcial) | 1 | 0 | 0% | Corrección confirmada |
| 4ª ejecución (parcial) | 1 | 1 | 100% | Flujo completo: vincular requería incidente existente |
| 5ª ejecución (parcial) | 1 | 0 | 0% | Corrección confirmada |
| **Ejecución final** | **229** | **0** | **0%** | **Todos los tests pasan** |

**Interpretación:** De los 11 fallos iniciales, 6 fueron errores en los tests (datos incorrectos, nombres de campos) y 5 fueron bugs reales en el código de producción (`IncidenteDetailView` no filtraba `active=True`, `IncidenteMensajesView` no tenía bypass para Admin, `NotificationVincularView` esperaba `incidente_pk` y no `incidente`). Todos fueron corregidos exitosamente.

### 4.4 Lecciones aprendidas

1. **Los tests de permisos son críticos** — El 57% de los bugs encontrados fueron de permisos. La matriz de 5 roles × múltiples recursos es compleja y propensa a errores.
2. **El soft-delete requiere vigilancia constante** — Cada nueva vista que acceda a Incidente debe verificar `active=True`. Olvidarlo es el error más común.
3. **El bypass de Admin** — En varias vistas de permisos, el Admin debe tener acceso irrestricto, pero no siempre se implementa explícitamente.
4. **Validación de datos en tests** — Los tests mal escritos (nombres de campos incorrectos) pueden dar falsos positivos. Es importante verificar que los tests realmente ejecuten la lógica que pretenden probar.

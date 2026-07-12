def roles_usuario(request):
    # funcion que debe retornar un diccionario con:
        # es_admin, es_supervisor, es_especialista, es_usuario, es_alta_gerencia
        # si el usuario no está autenticado, todos deben ser False
    return {
        'es_admin': request.user.groups.filter(name='Administrador').exists(),
        'es_supervisor': request.user.groups.filter(name='Supervisor').exists(),
        'es_especialista': request.user.groups.filter(name='Especialista').exists(),
        'es_usuario': request.user.groups.filter(name='Usuario').exists(),
        'es_alta_gerencia': request.user.groups.filter(name='Alta Gerencia').exists()
    } if request.user.is_authenticated else {
        'es_admin': False,
        'es_supervisor': False,
        'es_especialista': False,
        'es_usuario': False,
        'es_alta_gerencia': False
    }


def mensajes_no_leidos(request):
    if not request.user.is_authenticated:
        return {'mensajes_no_leidos': 0, 'incidentes_con_mensajes': [], 'notificaciones_respuestas': []}
    from django.db.models import Q, Prefetch
    from incidents.models import MensajeIncidente, Incidente
    from notifications.models import Notificacion
    user = request.user
    persona = user.perfil_persona
    if not persona:
        return {'mensajes_no_leidos': 0, 'incidentes_con_mensajes': [], 'notificaciones_respuestas': []}

    incidentes_data = []
    notificaciones_data = []

    if user.groups.filter(name__in=['Administrador', 'Supervisor', 'Especialista']).exists():
        incidentes_q = Q(supervisor=persona) | Q(especialista_asignado=persona)
        no_leidos = MensajeIncidente.objects.filter(
            Q(incidente__in=Incidente.objects.filter(incidentes_q).exclude(estado_incidente__code='CER')),
            leido=False
        ).exclude(remitente=persona).select_related('remitente', 'incidente')
        seen = set()
        for m in no_leidos:
            if m.incidente_id not in seen:
                seen.add(m.incidente_id)
                incidentes_data.append({
                    'pk': m.incidente.pk,
                    'codigo': m.incidente.codigo,
                    'titulo': m.incidente.titulo,
                    'remitente': f'{m.remitente.nombre} {m.remitente.apellidos}',
                })

    if user.groups.filter(name='Usuario').exists():
        notificaciones = Notificacion.objects.filter(
            usuario_notificador=user,
            respuesta_supervisor__isnull=False,
            incidente_asociado__isnull=False,
        ).exclude(respuesta_supervisor='').select_related('incidente_asociado')
        for n in notificaciones:
            notificaciones_data.append({
                'pk': n.pk,
                'asunto': n.asunto,
                'incidente_codigo': n.incidente_asociado.codigo,
                'respuesta_supervisor': n.respuesta_supervisor,
            })

    count = len(incidentes_data) + len(notificaciones_data)
    return {
        'mensajes_no_leidos': count,
        'incidentes_con_mensajes': incidentes_data,
        'notificaciones_respuestas': notificaciones_data,
    }
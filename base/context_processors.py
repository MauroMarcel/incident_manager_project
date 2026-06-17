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
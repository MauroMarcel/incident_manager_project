from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from incidents.models import Incidente
from notifications.models import Notificacion
from IoC.models import IoC
from users.models import Persona
from django.db.models import Q
from base.utils import get_areas_supervision


def custom_logout(request):
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def csrf_failure(request, reason=""):
    return render(request, '403.html', status=403)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):
        username = self.request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                form.errors['__all__'] = form.error_class(['CUENTA_INACTIVA'])
        except User.DoesNotExist:
            pass
        return super().form_invalid(form)


class AccesoDenegadoView(TemplateView):
    template_name = 'base/acceso_denegado.html'


class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        persona = getattr(user, 'perfil_persona', None)
        es_admin = user.groups.filter(name='Administrador').exists()
        es_supervisor = user.groups.filter(name='Supervisor').exists()
        es_especialista = user.groups.filter(name='Especialista').exists()
        es_gerencia = user.groups.filter(name='Alta Gerencia').exists()

        incidentes = Incidente.objects.filter(active=True)
        notificaciones = Notificacion.objects
        activo_queryset = Q(estado_incidente__code='INV')

        if es_admin:
            context['incidentes_activos'] = incidentes.filter(activo_queryset).count()
            context['notificaciones_pendientes'] = notificaciones.filter(estado_notificacion__code='PEN').count()
            context['total_iocs'] = IoC.objects.count()
            context['total_personas'] = Persona.objects.count()

        elif es_supervisor:
            context['incidentes_activos'] = incidentes.filter(activo_queryset).count()
            context['notificaciones_pendientes'] = notificaciones.filter(estado_notificacion__code='PEN').count()
            context['total_iocs'] = IoC.objects.count()
            context['total_personas'] = Persona.objects.count()

        elif es_gerencia:
            areas = get_areas_supervision(persona) if persona else []
            context['incidentes_activos'] = incidentes.filter(
                activo_queryset, areas_afectadas__in=areas
            ).distinct().count() if areas else 0
            context['notificaciones_pendientes'] = notificaciones.filter(
                estado_notificacion__code='PEN',
                area_notificacion__in=areas
            ).count() if areas else 0
            context['total_iocs'] = IoC.objects.count()
            context['total_personas'] = Persona.objects.filter(area__in=areas).count() if areas else 0

        elif es_especialista:
            context['incidentes_activos'] = incidentes.filter(
                activo_queryset, especialista_asignado=persona
            ).count() if persona else 0
            context['notificaciones_pendientes'] = notificaciones.filter(
                estado_notificacion__code__in=['PEN', 'REC'],
                usuario_notificador=user
            ).count()
            context['total_iocs'] = IoC.objects.count()
            context['total_personas'] = 0

        else:
            context['incidentes_activos'] = 0
            context['notificaciones_pendientes'] = notificaciones.filter(usuario_notificador=user).count() if user.is_authenticated else 0
            context['total_iocs'] = IoC.objects.count()
            context['total_personas'] = 0

        return context


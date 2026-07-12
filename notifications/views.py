from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from base.utils import get_areas_supervision
from base.mixins import RolRequeridoMixin
from references.models import Estado_Notificacion, Asunto_Notificacion
from .models import Notificacion, Evidencia_Notificacion
from .form import NotificacionForm
from incidents.models import Incidente
from .filters import NotificacionFilter

class NotificationCreateView(RolRequeridoMixin, CreateView):
    roles_permitidos = ['Usuario', 'Supervisor', 'Administrador', 'Especialista', 'Alta Gerencia']
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notifications/notification_form.html'

    def get_success_url(self):
        return reverse_lazy('notification-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asuntos'] = Asunto_Notificacion.objects.filter(active=True)
        return context

    def get_initial(self):
        initial = super().get_initial()
        persona = getattr(self.request.user, 'perfil_persona', None)
        if persona and persona.email:
            initial['email'] = persona.email
        return initial

    def form_valid(self, form):
        estado_inicial = Estado_Notificacion.objects.get(code='PEN')
        form.instance.estado_notificacion = estado_inicial
        form.instance.usuario_notificador = self.request.user
        response = super().form_valid(form)
        archivos = self.request.FILES.getlist('evidencias')
        for archivo in archivos:
            Evidencia_Notificacion.objects.create(
                notificacion=self.object,
                archivo=archivo
            )
        recipient = form.instance.email or self.request.user.email
        if recipient:
            send_mail(
                subject='Notificación recibida — SGIC',
                message=f'Su notificación sobre "{self.object.asunto}" fue registrada correctamente.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        else:
            messages.warning(
                self.request,
                'No se pudo enviar el correo de confirmación porque no tienes un email registrado.'
            )            
        return response


class NotificationDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Usuario', 'Supervisor', 'Administrador', 'Especialista', 'Alta Gerencia']
    model = Notificacion
    template_name = 'notifications/notification_detail.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        
        if request.user.groups.filter(name='Especialista').exists():
            notificacion = self.get_object()
            if notificacion.usuario_notificador == request.user:
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response
            if not notificacion.incidente_asociado or \
            notificacion.incidente_asociado.especialista_asignado != request.user.perfil_persona:
                return redirect ('acceso-denegado')
        
        if request.user.groups.filter(name='Alta Gerencia').exists():
            notificacion = self.get_object()
            from base.utils import get_areas_supervision
            areas = get_areas_supervision(request.user.perfil_persona)
            
            # Puede acceder si el área está supervisada O si fue él quien la creó
            if notificacion.area_notificacion not in areas and \
            notificacion.usuario_notificador != request.user:
                return redirect('acceso-denegado')
        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['incidentes'] = Incidente.objects.filter(titulo__icontains=q, estado_incidente__code__in=['ASI', 'INV'])
        context['q'] = q
        return context


class NotificationListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Usuario', 'Supervisor', 'Administrador', 'Especialista', 'Alta Gerencia']
    model = Notificacion
    template_name = 'notifications/notification_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_queryset(self):
        user = self.request.user
        # Primero se filtra por rol
        if user.groups.filter(name='Usuario').exists():
            queryset = Notificacion.objects.filter(usuario_notificador=user)
        elif user.groups.filter(name='Alta Gerencia').exists():
            areas = get_areas_supervision(user.perfil_persona)
            queryset = (Notificacion.objects.filter(
                area_notificacion__in=areas
            ) | Notificacion.objects.filter(
                usuario_notificador=user
            )).distinct()
        elif user.groups.filter(name='Especialista').exists():
            queryset = Notificacion.objects.filter(usuario_notificador=user)
        elif user.groups.filter(name='Supervisor').exists():
            queryset = Notificacion.objects.all()
        elif user.groups.filter(name='Administrador').exists():
            queryset = Notificacion.objects.all()
        else:
            queryset = Notificacion.objects.none()
        
        # Búsqueda semántica por asunto
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(asunto__icontains=q)
        
        # Luego se aplica el filtro de django_filters
        self.filterset = NotificacionFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['q'] = self.request.GET.get('q', '')
        return context


class NotificationRechazarView(RolRequeridoMixin, View):
    roles_permitidos = ['Supervisor', 'Administrador']
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        motivo = request.POST.get('motivo_rechazo')
        estado = Estado_Notificacion.objects.get(code='REC')
        notificacion.estado_notificacion = estado
        notificacion.respuesta_supervisor = motivo
        notificacion.save()
        recipient = notificacion.email or notificacion.usuario_notificador.email
        if recipient:
            send_mail(
                subject='Notificación rechazada — SGIC',
                message=f'Su notificación sobre "{notificacion.asunto}" fue rechazada.\nMotivo: {motivo}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        else:
            messages.warning(
                self.request,
                'No se pudo enviar el correo de confirmación porque no tienes un email registrado.'
            )
        return redirect('notification-detail', pk=pk)


class NotificationVincularView(RolRequeridoMixin, View):
    roles_permitidos = ['Supervisor', 'Administrador']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        incidente_pk = request.POST.get("incidente_pk")
        incidente = get_object_or_404(Incidente, active=True, pk=incidente_pk)
        notificacion.incidente_asociado = incidente
        estado_aceptada = Estado_Notificacion.objects.get(code='ACE')
        notificacion.estado_notificacion = estado_aceptada
        notificacion.save()
        if not incidente.areas_afectadas.filter(pk=notificacion.area_notificacion.pk).exists():
            incidente.areas_afectadas.add(notificacion.area_notificacion)
            messages.info(request, f'Se agregó el área "{notificacion.area_notificacion}" a las áreas afectadas del incidente.')
        recipient = notificacion.email or notificacion.usuario_notificador.email
        if recipient:
            send_mail(
                subject='Notificación aceptada — SGIC',
                message=f'Su notificación sobre "{notificacion.asunto}" está siendo investigada.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        else:
            messages.warning(
                self.request,
                'No se pudo enviar el correo de confirmación porque no tienes un email registrado.'
            )
        return redirect("notification-detail", pk=notificacion.pk)

class NotificacionEvidenciaCreateView(RolRequeridoMixin, View):
    roles_permitidos = ['Usuario', 'Especialista', 'Supervisor', 'Administrador']
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        
        # Verificar permisos del especialista
        if request.user.groups.filter(name='Especialista').exists():
            print(f"Usuario: {request.user}")
            print(f"Perfil persona: {request.user.perfil_persona}")
            print(f"Incidente asociado: {notificacion.incidente_asociado}")
            if notificacion.incidente_asociado:
                print(f"Especialista del incidente: {notificacion.incidente_asociado.especialista_asignado}")

            if not notificacion.incidente_asociado or \
            notificacion.incidente_asociado.especialista_asignado != request.user.perfil_persona:
                messages.warning(
                    request, 
                    'No tienes permiso para subir evidencias a esta notificación.',
                    extra_tags='notificacion'
                )
                return redirect('notification-detail', pk=pk)
        
        archivos = request.FILES.getlist('archivo')
        if archivos:
            for archivo in archivos:
                Evidencia_Notificacion.objects.create(
                    notificacion=notificacion,
                    archivo=archivo
                )
            messages.success(
                request,
                f'{len(archivos)} evidencia(s) subida(s) correctamente.',
                extra_tags='notificacion'
            )
        else:
            messages.warning(
                request, 
                'No se seleccionó ningún archivo.',
                extra_tags='notificacion'
            )
        return redirect('notification-detail', pk=pk)


class NotificacionDesvincularView(RolRequeridoMixin, View):
    roles_permitidos = ['Supervisor', 'Administrador']

    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        incidente_pk = notificacion.incidente_asociado.pk if notificacion.incidente_asociado else None
        notificacion.incidente_asociado = None
        estado_pendiente = Estado_Notificacion.objects.get(code='PEN')
        notificacion.estado_notificacion = estado_pendiente
        notificacion.save()
        messages.success(request, f'Notificación "{notificacion.asunto}" desvinculada del incidente.')
        if incidente_pk:
            return redirect('incidente-detalle', pk=incidente_pk)
        return redirect('notification-list')
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from incidents.models import Incidente
from references.models import Estado_Notificacion
from .models import Notificacion
from .form import NotificacionForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect

class NotificationCreateView(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notifications/notification_form.html'
    # Muestra los detalles de la notificacion despues de crearla
    def get_success_url(self):
        return reverse_lazy('notification-detail', kwargs={'pk': self.object.pk})
    
    # Asignar el estado inicial y el usuario notificador antes de guardar
    def form_valid(self, form):
        # Asignar estado inicial a la notificacion
        estado_inicial = Estado_Notificacion.objects.get(code='PEN')
        form.instance.estado_notificacion = estado_inicial
        # Guardar el usuario notificador (el usuario que crea la notificación)
        form.instance.usuario_notificador = self.request.user
        messages.success(self.request, "Notificación creada correctamente")
        return super().form_valid(form)


class NotificationDetailView(DetailView):
    model = Notificacion
    template_name = 'notifications/notification_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['incidentes'] = Incidente.objects.filter(
            titulo__icontains=q
        )
        context['q'] = q
        return context

class NotificationListView(ListView):
    model = Notificacion
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Usuario').exists():
            # Solo ve las suyas
            return Notificacion.objects.filter(usuario_notificador=user)
        if user.groups.filter(name='Alta Gerencia').exists():
            # Ve todas las de su area y areas subordinadas
            return Notificacion.objects.all()
        if user.groups.filter(name='Supervisor').exists():
            # Ve todas
            return Notificacion.objects.all()
        if user.groups.filter(name='Administrador').exists():
            # Ve todas
            return Notificacion.objects.all()
    template_name = 'notifications/notification_list.html'

class NotificationRechazarView(View):
    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        motivo = request.POST.get('motivo_rechazo')
        # aquí cambias el estado y guardas el motivo
        estado = Estado_Notificacion.objects.get(code='REC')
        notificacion.estado_notificacion = estado
        notificacion.respuesta_supervisor = motivo
        notificacion.save()
        return redirect('notification-detail', pk=pk)
    
class NotificationVincularView(View):
    def post(self, request, pk):
        notificacion = get_object_or_404(Notificacion, pk=pk)
        incidente_pk = request.POST.get("incidente_pk")

        incidente = get_object_or_404(Incidente, pk=incidente_pk)

        # Vincular
        notificacion.incidente_asociado = incidente
        estado_aceptada = Estado_Notificacion.objects.get(code='ACE')
        notificacion.estado_notificacion = estado_aceptada
        notificacion.save()
        # Advertencia para Supervisor acerca de la coincidencia de las areas
        if notificacion.area_notificacion != incidente.area_afectada:
            messages.warning(
                request,
                f'Advertencia: el área de la notificación '
                f'({notificacion.area_notificacion}) no coincide '
                f'con el área del incidente ({incidente.area_afectada}). '
                f'Notificación: {notificacion.pk}'
            )
        return redirect("notification-detail", pk=notificacion.pk)
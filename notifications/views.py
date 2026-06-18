from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
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
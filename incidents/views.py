from django.shortcuts import render
from notifications.models import Notificacion
from references.models import Estado_Incidente
from .models import Incidente
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from .forms import IncidenteForm


class IncidenteCreateView(CreateView):
    model = Incidente
    template_name = 'incidents/incident_form.html'
    form_class = IncidenteForm
    success_url = '#'
    def get_initial(self):
        notificacion = get_object_or_404(Notificacion, pk=self.kwargs['notificacion_pk'])
        return {
        'descripcion': notificacion.descripcion,
        'area_afectada': notificacion.area_notificacion,
    }
    def form_valid(self, form):
        notificacion = get_object_or_404(Notificacion, pk=self.kwargs['notificacion_pk'])
        form.instance.supervisor = self.request.user.perfil_persona
        form.instance.estado_incidente = Estado_Incidente.objects.get(code='REP')
        form.instance.fecha_reportado = notificacion.fecha_notificacion# fecha de la notificacion
        notificacion.incidente_asociado = form.instance
        notificacion.save()
        return super().form_valid(form)

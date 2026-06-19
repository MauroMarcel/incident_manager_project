from notifications.models import Notificacion
from .models import Incidente
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect, render
from references.models import Estado_Incidente, Estado_Notificacion
from django.views import View
from .forms import IncidenteForm, IncidenteReporteOficialForm, IncidenteClasificacionInternaForm, IncidenteTemporalidadForm
from django.views.generic import ListView
from django.db.models import Count, Q
from django.contrib.auth.models import Group
from users.models import Persona
from django.utils import timezone

def get_especialistas_ordenados(incidente):
    grupo_especialista = Group.objects.get(name='Especialista')
    
    # Determinar el filtro de experiencia
    if incidente.tipo_incidente:
        filtro_exp = Q(
            especialistas_incidente__tipo_incidente=incidente.tipo_incidente,
            especialistas_incidente__estado_incidente__code='RES'
        )
    elif incidente.notificaciones_incidente.exists():
        asunto = incidente.notificaciones_incidente.first().asunto
        filtro_exp = Q(
            especialistas_incidente__notificaciones_incidente__asunto=asunto,
            especialistas_incidente__estado_incidente__code='RES'
        )
    else:
        filtro_exp = Q(
            especialistas_incidente__estado_incidente__code='RES'
        )
    
    return Persona.objects.filter(
        usuario_django__groups=grupo_especialista,
        estado_persona__code='ACT'
    ).annotate(
        exp_tipo=Count('especialistas_incidente', filter=filtro_exp),
        casos_activos=Count(
            'especialistas_incidente',
            filter=~Q(especialistas_incidente__estado_incidente__code__in=['RES','REC'])
        ),
        total_resueltos=Count(
            'especialistas_incidente',
            filter=Q(especialistas_incidente__estado_incidente__code='RES')
        )
    ).order_by('-exp_tipo', 'casos_activos', '-total_resueltos')
class IncidenteAsignarEspecialistaView(View):
    def get(self, request, pk):
        incidente = get_object_or_404(Incidente, pk=pk)
        especialistas = get_especialistas_ordenados(incidente)
        return render(request, 'incidents/asignar_especialista.html', {
            'incidente': incidente,
            'especialistas': especialistas,
        })
    
    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, pk=pk)
        especialista_pk = request.POST.get('especialista_pk')
        especialista = get_object_or_404(Persona, pk=especialista_pk)
        incidente.especialista_asignado = especialista
        # cambiar estado a ASI
        incidente.estado_incidente = Estado_Incidente.objects.get(code='ASI')
        incidente.fecha_asignacion = timezone.now()
        incidente.save()
        return redirect('incidente-lista')

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
        form.instance.fecha_reportado = notificacion.fecha_notificacion
        response = super().form_valid(form)  
        notificacion.incidente_asociado = self.object
        estado_aceptada = Estado_Notificacion.objects.get(code='ACE')
        notificacion.estado_notificacion = estado_aceptada
        notificacion.save()
        return response

class IncidenteWizardView(View):
    
    PASOS = {
        '1': IncidenteReporteOficialForm,
        '2': IncidenteClasificacionInternaForm,
        '3': IncidenteTemporalidadForm,
    }
    
    def get(self, request, pk, paso='1'):
        incidente = get_object_or_404(Incidente, pk=pk)
        FormClass = self.PASOS[paso]
        form = FormClass(instance=incidente)
        return render(request, 'incidents/wizard.html', {
            'form': form,
            'paso': paso,
            'paso_anterior': str(int(paso) - 1),
            'incidente': incidente,
            'total_pasos': len(self.PASOS),
            'porcentaje': int(paso) * 100 // len(self.PASOS)
        })
    
    def post(self, request, pk, paso='1'):
        incidente = get_object_or_404(Incidente, pk=pk)
        FormClass = self.PASOS[paso]
        form = FormClass(request.POST, instance=incidente)
        
        if form.is_valid():
            form.save()
            siguiente = str(int(paso) + 1)
            if siguiente in self.PASOS:
                return redirect('incidente-wizard', pk=pk, paso=siguiente)
            return redirect('incidente-lista')
        
        return render(request, 'incidents/wizard.html', {
            'form': form,
            'paso': paso,
            'paso_anterior': str(int(paso) - 1),
            'incidente': incidente,
            'total_pasos': len(self.PASOS),
            'porcentaje': int(paso) * 100 // len(self.PASOS)
        })

class IncidenteListView(ListView):
    model = Incidente
    template_name = 'incidents/incident_list.html'
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Especialista').exists():
            # Solo los suyos y activos
            return Incidente.objects.filter(especialista_asignado=self.request.user.perfil_persona).exclude(estado_incidente__code='REC')
        if user.groups.filter(name='Supervisor').exists():
            # Todos
            return Incidente.objects.all()
        if user.groups.filter(name='Administrador').exists():
            # Todos
            return Incidente.objects.all()
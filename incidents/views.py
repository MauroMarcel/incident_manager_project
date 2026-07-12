from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q, Value, IntegerField
from django.contrib.auth.models import Group
from django.contrib import messages
from base.mixins import RolRequeridoMixin
from notifications.models import Notificacion
from references.models import Estado_Incidente, Estado_Notificacion
from users.models import Persona
from .models import Incidente, Evidencia_Incidente, MensajeIncidente
from .forms import IncidenteForm, IncidenteReporteOficialForm, IncidenteClasificacionInternaForm, IncidenteTemporalidadForm, MensajeIncidenteForm
from base.utils import get_areas_supervision
from .filters import IncidenteFilter

def get_especialistas_ordenados(incidente=None):
    grupo_especialista = Group.objects.get(name='Especialista')
    
    if incidente and incidente.tipo_incidente:
        filtro_exp = Q(
            especialistas_incidente__tipo_incidente=incidente.tipo_incidente,
            especialistas_incidente__estado_incidente__code='CER'
        )
    elif incidente and incidente.notificaciones_incidente.exists():
        asunto = incidente.notificaciones_incidente.first().asunto
        filtro_exp = Q(
            especialistas_incidente__notificaciones_incidente__asunto=asunto,
            especialistas_incidente__estado_incidente__code='CER'
        )
    else:
        filtro_exp = Q(
            especialistas_incidente__estado_incidente__code='CER'
        )
    
    return Persona.objects.filter(
        usuario_django__groups=grupo_especialista,
        estado_persona__code='ACT'
    ).annotate(
        exp_tipo=Count('especialistas_incidente', filter=filtro_exp),
        casos_activos=Count(
            'especialistas_incidente',
            filter=Q(especialistas_incidente__estado_incidente__code='INV')
        ),
        total_resueltos=Count(
            'especialistas_incidente',
            filter=Q(especialistas_incidente__estado_incidente__code='CER')
        )
    ).order_by('-exp_tipo', 'casos_activos', '-total_resueltos')


class IncidenteListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador', 'Alta Gerencia']
    model = Incidente
    template_name = 'incidents/incident_list.html'


    def get_queryset(self):
        user = self.request.user
        base = Incidente.objects.filter(active=True)
        if user.groups.filter(name='Alta Gerencia').exists():
            areas = get_areas_supervision(user.perfil_persona)
            queryset= base.filter(areas_afectadas__in=areas).distinct()
        elif user.groups.filter(name='Especialista').exists():
            queryset= base.filter(especialista_asignado=user.perfil_persona)
        elif user.groups.filter(name='Supervisor').exists():
            queryset= base.filter(supervisor=user.perfil_persona)
        elif user.groups.filter(name='Administrador').exists():
            queryset= base.all()
        else:
            queryset = Incidente.objects.none()
        
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(titulo__icontains=q)
        
        self.filterset = IncidenteFilter(self.request.GET, queryset=queryset)
        qs = self.filterset.qs.select_related('supervisor', 'especialista_asignado')
        persona = self.request.user.perfil_persona
        if persona and persona.pk:
            qs = qs.annotate(
                mensajes_no_leidos=Count(
                    'mensajes',
                    filter=Q(mensajes__leido=False) & ~Q(mensajes__remitente=persona)
                )
            )
        else:
            qs = qs.annotate(mensajes_no_leidos=Value(0, output_field=IntegerField()))
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['q'] = self.request.GET.get('q', '')
        return context


class IncidenteCreateView(RolRequeridoMixin, CreateView):
    roles_permitidos = ['Supervisor', 'Administrador']
    model = Incidente
    template_name = 'incidents/incident_form.html'
    form_class = IncidenteForm
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_success_url(self):
        return reverse_lazy('incidente-lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notificacion'] = get_object_or_404(Notificacion, pk=self.kwargs['notificacion_pk'])
        context['especialistas'] = get_especialistas_ordenados()
        return context

    def get_initial(self):
        notificacion = get_object_or_404(Notificacion, pk=self.kwargs['notificacion_pk'])
        return {
            'descripcion': notificacion.descripcion,
            'areas_afectadas': [notificacion.area_notificacion],
        }

    def form_valid(self, form):
        notificacion = get_object_or_404(Notificacion, pk=self.kwargs['notificacion_pk'])
        
        # PRIMERO verificar si ya tiene incidente asociado
        if notificacion.incidente_asociado:
            messages.warning(
                self.request,
                f'Esta notificación ya está asociada al incidente {notificacion.incidente_asociado.codigo}.'
            )
            return redirect('notification-detail', pk=notificacion.pk)
        
        # LUEGO verificar duplicado
        areas = form.cleaned_data.get('areas_afectadas')
        incidente_similar = Incidente.objects.filter(
            titulo=form.cleaned_data['titulo']
        ).filter(areas_afectadas__in=areas).exists()
        if incidente_similar:
            messages.warning(
                self.request,
                'Advertencia: ya existe un incidente con el mismo título y área afectada.'
            )
        
        # LUEGO guardar
        form.instance.supervisor = self.request.user.perfil_persona
        form.instance.estado_incidente = Estado_Incidente.objects.get(code='ASI')
        form.instance.fecha_reportado = notificacion.fecha_notificacion
        response = super().form_valid(form)
        
        notificacion.incidente_asociado = self.object
        estado_aceptada = Estado_Notificacion.objects.get(code='ACE')
        notificacion.estado_notificacion = estado_aceptada
        notificacion.save()
        
        if notificacion.usuario_notificador.email:
            send_mail(
                subject='Notificación aceptada — SGIC',
                message=f'Su notificación sobre "{notificacion.asunto}" está siendo investigada.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notificacion.usuario_notificador.email],
                fail_silently=False,
            )
        else:
            messages.warning(
                self.request,
                'No se pudo enviar el correo de confirmación porque el usuario no tiene email registrado.'
            )
        
        return response


class IncidenteCreateDirectView(RolRequeridoMixin, CreateView):
    roles_permitidos = ['Supervisor', 'Administrador']
    model = Incidente
    template_name = 'incidents/incident_form_direct.html'
    form_class = IncidenteForm

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_success_url(self):
        return reverse_lazy('incidente-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialistas'] = get_especialistas_ordenados()
        return context

    def form_valid(self, form):
        form.instance.supervisor = self.request.user.perfil_persona
        form.instance.estado_incidente = Estado_Incidente.objects.get(code='ASI')
        form.instance.fecha_reportado = timezone.now()
        return super().form_valid(form)


class IncidenteDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador', 'Alta Gerencia']
    model = Incidente
    template_name = 'incidents/incident_detail.html'

    def get_queryset(self):
        return Incidente.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notificacion_origen'] = self.object.notificaciones_incidente.order_by('created').first()
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        
        # Verificación de especialista asignado
        if request.user.groups.filter(name='Especialista').exists():
            incidente = self.get_object()
            if incidente.especialista_asignado != request.user.perfil_persona:
                return redirect('acceso-denegado')
        
        # Verificación de Alta Gerencia
        if request.user.groups.filter(name='Alta Gerencia').exists():
            incidente = self.get_object()
            from base.utils import get_areas_supervision
            areas = get_areas_supervision(request.user.perfil_persona)
            if not incidente.areas_afectadas.filter(pk__in=[a.pk for a in areas]).exists():
                return redirect('acceso-denegado')
        
        # Deshabilitar caché
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class IncidenteWizardView(RolRequeridoMixin, View):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador']

    PASOS = {
        '1': IncidenteReporteOficialForm,
        '2': IncidenteClasificacionInternaForm,
        '3': IncidenteTemporalidadForm,
    }
    def dispatch(self, request, *args, **kwargs):
        incidente = get_object_or_404(Incidente, active=True, pk=self.kwargs['pk'])
        if incidente.estado_incidente.code == 'CER':
            messages.warning(request, 'No puedes modificar un incidente cerrado.')
            return redirect('incidente-detalle', pk=incidente.pk)
        if request.user.groups.filter(name='Especialista').exists():
            if incidente.especialista_asignado != request.user.perfil_persona:
                return redirect('acceso-denegado')
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get(self, request, pk, paso='1'):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        
        # Cambiar estado a "En Investigación" si está asignado
        if incidente.estado_incidente.code == 'ASI':
            incidente.estado_incidente = Estado_Incidente.objects.get(code='INV')
            incidente.save()
        
        FormClass = self.PASOS[paso]
        form = FormClass(instance=incidente)
        
        context = {
            'form': form,
            'paso': paso,
            'paso_anterior': str(int(paso) - 1),
            'incidente': incidente,
            'total_pasos': len(self.PASOS),
            'porcentaje': int(paso) * 100 // len(self.PASOS)
        }
        
        return render(request, 'incidents/wizard.html', context)

    def post(self, request, pk, paso='1'):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        FormClass = self.PASOS[paso]
        form = FormClass(request.POST, instance=incidente)
        
        if form.is_valid():  
            form.save()
            
            # Si es el paso de temporalidad y hay fecha de solución → marcar como Cerrado
            if paso == '3' and form.cleaned_data.get('fecha_solucion'):
                incidente.estado_incidente = Estado_Incidente.objects.get(code='CER')
                incidente.save()
            
            # Avanzar al siguiente paso o redirigir al detalle
            siguiente = str(int(paso) + 1)
            if siguiente in self.PASOS:
                return redirect('incidente-wizard', pk=pk, paso=siguiente)
            return redirect('incidente-detalle', pk=pk)
        
        # Si el formulario no es válido — re-renderizar con errores
        context = {
            'form': form,
            'paso': paso,
            'paso_anterior': str(int(paso) - 1),
            'incidente': incidente,
            'total_pasos': len(self.PASOS),
            'porcentaje': int(paso) * 100 // len(self.PASOS)
        }
        
        return render(request, 'incidents/wizard.html', context)


class IncidenteAsignarEspecialistaView(RolRequeridoMixin, View):
    roles_permitidos = ['Supervisor', 'Administrador']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get(self, request, pk):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        especialistas = get_especialistas_ordenados(incidente)
        return render(request, 'incidents/asignar_especialista.html', {
            'incidente': incidente,
            'especialistas': especialistas,
        })

    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        especialista_pk = request.POST.get('especialista_pk')
        especialista = get_object_or_404(Persona, pk=especialista_pk)
        incidente.especialista_asignado = especialista
        incidente.estado_incidente = Estado_Incidente.objects.get(code='ASI')
        incidente.fecha_asignacion = timezone.now()
        incidente.save()
        return redirect('incidente-lista')

class IncidenteReasignarEspecialistaView(RolRequeridoMixin, View):
    roles_permitidos = ['Supervisor', 'Administrador']

    def post(self, request, pk):
        return redirect('incidente-asignar', pk=pk)

class IncidenteCambiarEstadoView(RolRequeridoMixin, View):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        nuevo_estado = request.POST.get('estado')
        persona = request.user.perfil_persona
        es_especialista = request.user.groups.filter(name='Especialista').exists()
        es_supervisor = request.user.groups.filter(name='Supervisor').exists()

        if es_especialista:
            if incidente.especialista_asignado != persona:
                messages.warning(request, 'No tienes permiso para cambiar el estado de este incidente.')
                return redirect('incidente-detalle', pk=pk)
        if es_supervisor:
            if incidente.supervisor != persona:
                messages.warning(request, 'No tienes permiso para cambiar el estado de este incidente.')
                return redirect('incidente-detalle', pk=pk)

        if nuevo_estado == 'ASI':
            if incidente.estado_incidente.code == 'CER':
                incidente.fecha_solucion = None
            incidente.estado_incidente = Estado_Incidente.objects.get(code='ASI')
            messages.success(request, f'Incidente {incidente.codigo} marcado como Asignado.', extra_tags='incidente')
        elif nuevo_estado == 'INV':
            if incidente.estado_incidente.code == 'CER':
                incidente.fecha_solucion = None
            incidente.estado_incidente = Estado_Incidente.objects.get(code='INV')
            messages.success(request, f'Incidente {incidente.codigo} marcado como Investigado.', extra_tags='incidente')
        elif nuevo_estado == 'CER':
            incidente.estado_incidente = Estado_Incidente.objects.get(code='CER')
            incidente.fecha_solucion = timezone.now()
            messages.success(request, f'Incidente {incidente.codigo} cerrado correctamente.', extra_tags='incidente')
            mensaje_contenido = request.POST.get('mensaje_contenido', '').strip()
            if mensaje_contenido:
                MensajeIncidente.objects.create(
                    incidente=incidente,
                    remitente=persona,
                    contenido=mensaje_contenido
                )
                estado_res, _ = Estado_Notificacion.objects.get_or_create(
                    code='RES', defaults={'name': 'Resuelta'}
                )
                for notif in incidente.notificaciones_incidente.all():
                    notif.respuesta_supervisor = mensaje_contenido
                    notif.estado_notificacion = estado_res
                    notif.save()
                    recipient = notif.email or notif.usuario_notificador.email
                    if recipient:
                        send_mail(
                            subject='Notificación resuelta — SGIC',
                            message=f'Su notificación sobre "{notif.asunto}" ha sido resuelta.\n\nMensaje del supervisor:\n{mensaje_contenido}',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[recipient],
                            fail_silently=False,
                        )
        else:
            messages.warning(request, 'Estado no válido.')
            return redirect('incidente-detalle', pk=pk)

        incidente.save()
        return redirect('incidente-detalle', pk=pk)

class IncidenteEvidenciaCreateView(RolRequeridoMixin, View):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador']
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, active=True, pk=pk)
        if request.user.groups.filter(name='Especialista').exists():
            if incidente.especialista_asignado != request.user.perfil_persona:
                messages.warning(request, 'No tienes permiso para subir evidencias a este incidente.')
                return redirect('incidente-detalle', pk=pk)
        archivos = request.FILES.getlist('archivo')
        if archivos:
            for archivo in archivos:
                Evidencia_Incidente.objects.create(
                    incidente=incidente,
                    archivo=archivo
                )
            messages.success(request, f'{len(archivos)} evidencia(s) subida(s) correctamente.', extra_tags='incidente')
        else:
            messages.warning(request, 'No se seleccionó ningún archivo.')
        return redirect(reverse_lazy('incidente-detalle', kwargs={'pk': pk}) + '?tab=evidencias')


class IncidenteMensajesView(RolRequeridoMixin, View):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_incidente(self):
        return get_object_or_404(Incidente, active=True, pk=self.kwargs['pk'])

    def verificar_acceso(self, request, incidente):
        if request.user.groups.filter(name='Administrador').exists():
            return
        persona = request.user.perfil_persona
        if not (incidente.supervisor == persona or incidente.especialista_asignado == persona):
            raise Http404

    def verificar_incidente_cerrado(self, request, incidente):
        if incidente.estado_incidente.code == 'CER':
            from django.contrib import messages
            messages.warning(request, 'El canal de comunicación está cerrado porque el incidente se encuentra en estado "Cerrado".')
            return redirect('incidente-detalle', pk=incidente.pk)

    def get(self, request, pk):
        incidente = self.get_incidente()
        self.verificar_acceso(request, incidente)
        resp = self.verificar_incidente_cerrado(request, incidente)
        if resp:
            return resp
        messages_qs = incidente.mensajes.all()
        form = MensajeIncidenteForm()
        MensajeIncidente.objects.filter(
            incidente=incidente
        ).exclude(
            remitente=request.user.perfil_persona
        ).update(leido=True)
        return render(request, 'incidents/incident_mensajes.html', {
            'incidente': incidente,
            'mensajes': messages_qs,
            'form': form,
        })

    def post(self, request, pk):
        incidente = self.get_incidente()
        self.verificar_acceso(request, incidente)
        resp = self.verificar_incidente_cerrado(request, incidente)
        if resp:
            return resp
        form = MensajeIncidenteForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.incidente = incidente
            mensaje.remitente = request.user.perfil_persona
            mensaje.save()
            return redirect('incidente-mensajes', pk=pk)
        messages_qs = incidente.mensajes.all()
        return render(request, 'incidents/incident_mensajes.html', {
            'incidente': incidente,
            'mensajes': messages_qs,
            'form': form,
        })


class EvidenciaIncidenteDeleteView(RolRequeridoMixin, View):
    roles_permitidos = ['Especialista', 'Supervisor', 'Administrador']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def post(self, request, pk):
        evidencia = get_object_or_404(Evidencia_Incidente, pk=pk)
        incidente = evidencia.incidente
        if not request.user.groups.filter(name='Administrador').exists():
            if request.user.groups.filter(name='Supervisor').exists():
                if incidente.supervisor != request.user.perfil_persona:
                    messages.warning(request, 'No tienes permiso para eliminar evidencias de este incidente.')
                    return redirect(reverse_lazy('incidente-detalle', kwargs={'pk': incidente.pk}) + '?tab=evidencias')
            else:
                messages.warning(request, 'No tienes permiso para eliminar evidencias.')
                return redirect(reverse_lazy('incidente-detalle', kwargs={'pk': incidente.pk}) + '?tab=evidencias')
        evidencia.archivo.delete()
        evidencia.delete()
        messages.success(request, 'Evidencia eliminada correctamente.', extra_tags='incidente')
        return redirect(reverse_lazy('incidente-detalle', kwargs={'pk': incidente.pk}) + '?tab=evidencias')


class IncidenteDeletedListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Administrador', 'Supervisor']
    model = Incidente
    template_name = 'incidents/incidente_deleted_list.html'
    context_object_name = 'incidentes'

    def get_queryset(self):
        user = self.request.user
        qs = Incidente.objects.filter(active=False)
        if user.groups.filter(name='Supervisor').exists():
            qs = qs.filter(supervisor=user.perfil_persona)
        return qs.order_by('-updated')


class IncidenteRestoreView(RolRequeridoMixin, View):
    roles_permitidos = ['Administrador', 'Supervisor']

    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, pk=pk, active=False)
        if request.user.groups.filter(name='Supervisor').exists():
            if incidente.supervisor != request.user.perfil_persona:
                messages.warning(request, 'No tienes permiso para restaurar este incidente.')
                return redirect('incidente-eliminados-lista')
        incidente.active = True
        incidente.save()
        messages.success(request, f'Incidente "{incidente.codigo}" restaurado correctamente.')
        return redirect('incidente-eliminados-lista')


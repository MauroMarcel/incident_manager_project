from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from base.mixins import RolRequeridoMixin
from .models import Persona
from .forms import PersonaForm
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from references.models import Estado_Persona
from incidents.models import Incidente

class PersonaCreateView(RolRequeridoMixin, CreateView):
    roles_permitidos = ['Administrador']
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'
    success_url = reverse_lazy('persona-lista')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def form_valid(self, form):
        persona = form.save(commit=False)
        persona.save()

        if form.cleaned_data.get('es_usuario'):
            rol = form.cleaned_data.get('rol')
            password = form.cleaned_data.get('password1')

            # Crear User de Django
            user = User.objects.create_user(
                username=persona.identificador_interno,
                password=password,
                email=persona.email or '',
                first_name=persona.nombre,
                last_name=persona.apellidos,
            )

            # Asignar permisos si es Administrador
            if rol.name == 'Administrador':
                user.is_staff = True
                user.is_superuser = True
            
            user.is_active = True
            user.save()

            # Asignar grupo/rol
            user.groups.add(rol)

            # Vincular User a Persona
            persona.usuario_django = user
            persona.save()

        return super().form_valid(form)



class PersonaListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Administrador']
    model = Persona
    template_name = 'users/persona_list.html'
    context_object_name = 'personas'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_queryset(self):
        mostrar = self.request.GET.get('mostrar', 'activas')
        if mostrar == 'inactivas':
            return Persona.objects.filter(active=False)
        return Persona.objects.filter(active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mostrar'] = self.request.GET.get('mostrar', 'activas')
        return context

class PersonaDeleteView(RolRequeridoMixin, View):
    roles_permitidos = ['Administrador']

    def post(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        
        # Verificar incidentes activos como especialista
        incidentes_activos = Incidente.objects.filter(
            especialista_asignado=persona,
        ).exclude(
            estado_incidente__code__in=['RES', 'REC']
        )
        
        if incidentes_activos.exists():
            messages.warning(
                request,
                f'Advertencia: {persona} tiene {incidentes_activos.count()} incidente(s) activo(s) asignado(s). '
                f'Reasigna los incidentes antes de desactivar esta persona.'
            )
            return redirect('persona-detalle', pk=pk)
        
        # Si no tiene incidentes activos procede con la desactivación
        persona.active = False
        persona.fecha_baja = timezone.now()
        persona.estado_persona = Estado_Persona.objects.get(code='INA')
        if persona.usuario_django:
            persona.usuario_django.is_active = False
            persona.usuario_django.save()
        persona.save()
        messages.success(request, f'{persona} fue desactivada correctamente.')
        return redirect('persona-lista')

class PersonaActivarView(RolRequeridoMixin, View):
    roles_permitidos = ['Administrador']

    def post(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        persona.active = True
        persona.fecha_baja = None
        persona.estado_persona = Estado_Persona.objects.get(code='ACT')
        if persona.usuario_django:
            persona.usuario_django.is_active = True
            persona.usuario_django.save()
        persona.save()
        messages.success(request, f'{persona} fue reactivada correctamente.')
        return redirect('persona-lista')


class PersonaDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Administrador']
    model = Persona
    template_name = 'users/persona_detail.html'
    context_object_name = 'persona'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
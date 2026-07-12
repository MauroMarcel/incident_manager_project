from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from base.mixins import RolRequeridoMixin
from .models import Persona, ConfiguracionAltaGerencia
from .forms import PersonaForm
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from references.models import Estado_Persona, Cargo
from incidents.models import Incidente
from organization.models import Area
from django.views.generic import UpdateView
from .forms import PersonaForm, PersonaUpdateForm


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

        if persona.estado_persona and persona.estado_persona.code == 'INA':
            persona.active = False
        elif persona.estado_persona and persona.estado_persona.code == 'ACT':
            persona.active = True

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
            
            user.is_active = persona.active
            user.save()

            # Asignar grupo/rol
            user.groups.add(rol)

            # Vincular User a Persona
            persona.usuario_django = user
            persona.save()

        return super().form_valid(form)



class PersonaListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Administrador', 'Alta Gerencia']
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
        queryset = Persona.objects.select_related('area', 'cargo')
        q = self.request.GET.get('q', '').strip()
        mostrar = self.request.GET.get('mostrar', 'activas')
        area = self.request.GET.get('area')
        cargo = self.request.GET.get('cargo')

        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(apellidos__icontains=q) |
                Q(identificador_interno__icontains=q)
            )

        if mostrar == 'activas':
            queryset = queryset.filter(active=True)
        elif mostrar == 'inactivas':
            queryset = queryset.filter(active=False)

        if area:
            queryset = queryset.filter(area_id=area)

        if cargo:
            queryset = queryset.filter(cargo_id=cargo)

        return queryset.order_by('apellidos', 'nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['mostrar'] = self.request.GET.get('mostrar', 'activas')
        context['selected_area'] = self.request.GET.get('area', '')
        context['selected_cargo'] = self.request.GET.get('cargo', '')
        context['areas'] = Area.objects.all()
        context['cargos'] = Cargo.objects.filter(active=True)
        return context

class PersonaDeleteView(RolRequeridoMixin, View):
    roles_permitidos = ['Administrador']

    def post(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        
        # Evitar que el admin se desactive a sí mismo
        if persona.usuario_django == request.user:
            messages.warning(
                request,
                'No puedes desactivarte a ti mismo.'
            )
            return redirect('persona-detalle', pk=pk)
        # Verificar incidentes activos como especialista
        incidentes_activos = Incidente.objects.filter(
            especialista_asignado=persona,
            estado_incidente__code='INV'
        )
        # Verificar incidentes activos como supervisor
        incidentes_supervisados = Incidente.objects.filter(
            supervisor=persona,
            estado_incidente__code='INV'
        )

        if incidentes_supervisados.exists():
            codigos = ', '.join([i.codigo for i in incidentes_supervisados])
            messages.warning(
                request,
                f'{persona} supervisa incidentes activos: {codigos}. '
                f'Reasigna estos incidentes antes de desactivar.'
            )
            return redirect('persona-detalle', pk=pk)
        if incidentes_activos.exists():
            codigos = ', '.join([i.codigo for i in incidentes_activos])
            messages.warning(
                request,
                f'{persona} tiene incidentes activos asignados: {codigos}. '
                f'Reasigna estos incidentes antes de desactivar esta persona.'
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



class PersonaUpdateView(RolRequeridoMixin, UpdateView):
    roles_permitidos = ['Administrador']
    model = Persona
    form_class = PersonaUpdateForm
    template_name = 'users/persona_form.html'

    def get_success_url(self):
        return reverse_lazy('persona-detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        persona = form.save(commit=False)
        
        # Sincronizar active con estado_persona
        if persona.estado_persona and persona.estado_persona.code == 'INA':
            persona.active = False
            if persona.usuario_django:
                persona.usuario_django.is_active = False
                persona.usuario_django.save()
        elif persona.estado_persona and persona.estado_persona.code == 'ACT':
            persona.active = True
            if persona.usuario_django:
                persona.usuario_django.is_active = True
                persona.usuario_django.save()
        
        # Actualizar email en User de Django si existe
        if persona.usuario_django and 'email' in form.changed_data:
            persona.usuario_django.email = persona.email
            persona.usuario_django.save()
        
        persona.save()
        messages.success(self.request, f'{persona} actualizada correctamente.')
        return super().form_valid(form)

class PersonaDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Administrador', 'Alta Gerencia']
    model = Persona
    template_name = 'users/persona_detail.html'
    context_object_name = 'persona'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        persona = self.object
        if persona.usuario_django and persona.usuario_django.groups.filter(name='Especialista').exists():
            stats = Persona.objects.filter(pk=persona.pk).annotate(
                total_casos=Count('especialistas_incidente'),
                casos_activos=Count(
                    'especialistas_incidente',
                    filter=Q(especialistas_incidente__estado_incidente__code='INV')
                ),
                total_resueltos=Count(
                    'especialistas_incidente',
                    filter=Q(especialistas_incidente__estado_incidente__code='CER')
                )
            ).first()
            context['total_casos'] = stats.total_casos if stats else 0
            context['casos_activos'] = stats.casos_activos if stats else 0
            context['total_resueltos'] = stats.total_resueltos if stats else 0
        return context


class PersonaConfigurarAreasView(RolRequeridoMixin, View):
    roles_permitidos = ['Administrador', 'Alta Gerencia']

    def post(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        config, _ = ConfiguracionAltaGerencia.objects.get_or_create(persona=persona)
        area_ids = request.POST.getlist('areas')
        config.areas_supervision.set(area_ids)
        messages.success(
            request,
            f'Áreas de supervisión actualizadas para {persona.nombre} {persona.apellidos}.'
        )
        return redirect('persona-detalle', pk=pk)


class MiPerfilView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'users/mi_perfil.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persona'] = getattr(self.request.user, 'perfil_persona', None)
        return context
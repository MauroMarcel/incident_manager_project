from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from base.mixins import RolRequeridoMixin
from .models import Persona
from .forms import PersonaForm
from django.views.generic import ListView
from django.views.generic import DetailView

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
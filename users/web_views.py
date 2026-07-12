from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Persona, Categoria_Persona, Cargo, Estado_Persona, ConfiguracionAltaGerencia
from organization.models import Area
from .forms import (
    PersonaForm, Categoria_PersonaForm, CargoForm, Estado_PersonaForm
)


# ==================== CATEGORIA_PERSONA VIEWS ====================

class Categoria_PersonaListView(LoginRequiredMixin, ListView):
    """Lista todas las categorías de personas con búsqueda y filtrado"""
    model = Categoria_Persona
    template_name = 'users/categoria_persona_list.html'
    context_object_name = 'categorias'
    paginate_by = 20

    def get_queryset(self):
        queryset = Categoria_Persona.objects.all()
        search = self.request.GET.get('search')
        active = self.request.GET.get('active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        if active == 'true':
            queryset = queryset.filter(active=True)
        elif active == 'false':
            queryset = queryset.filter(active=False)
        
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['active_filter'] = self.request.GET.get('active', '')
        return context


class Categoria_PersonaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una categoría de persona"""
    model = Categoria_Persona
    template_name = 'users/categoria_persona_detail.html'
    context_object_name = 'categoria'


class Categoria_PersonaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva categoría de persona"""
    model = Categoria_Persona
    form_class = Categoria_PersonaForm
    template_name = 'users/categoria_persona_form.html'
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Categoría "{form.instance.name}" creada exitosamente.')
        return response


class Categoria_PersonaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar categoría de persona"""
    model = Categoria_Persona
    form_class = Categoria_PersonaForm
    template_name = 'users/categoria_persona_form.html'
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Categoría "{form.instance.name}" actualizada exitosamente.')
        return response


class Categoria_PersonaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar categoría de persona"""
    model = Categoria_Persona
    template_name = 'users/categoria_persona_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Categoría "{name}" eliminada exitosamente.')
        return response


# ==================== CARGO VIEWS ====================

class CargoListView(LoginRequiredMixin, ListView):
    """Lista todos los cargos con búsqueda y filtrado"""
    model = Cargo
    template_name = 'users/cargo_list.html'
    context_object_name = 'cargos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Cargo.objects.all()
        search = self.request.GET.get('search')
        active = self.request.GET.get('active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        if active == 'true':
            queryset = queryset.filter(active=True)
        elif active == 'false':
            queryset = queryset.filter(active=False)
        
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['active_filter'] = self.request.GET.get('active', '')
        return context


class CargoDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un cargo"""
    model = Cargo
    template_name = 'users/cargo_detail.html'
    context_object_name = 'cargo'


class CargoCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo cargo"""
    model = Cargo
    form_class = CargoForm
    template_name = 'users/cargo_form.html'
    success_url = reverse_lazy('cargo-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Cargo "{form.instance.name}" creado exitosamente.')
        return response


class CargoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar cargo"""
    model = Cargo
    form_class = CargoForm
    template_name = 'users/cargo_form.html'
    success_url = reverse_lazy('cargo-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Cargo "{form.instance.name}" actualizado exitosamente.')
        return response


class CargoDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar cargo"""
    model = Cargo
    template_name = 'users/cargo_confirm_delete.html'
    success_url = reverse_lazy('cargo-list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Cargo "{name}" eliminado exitosamente.')
        return response


# ==================== ESTADO_PERSONA VIEWS ====================

class Estado_PersonaListView(LoginRequiredMixin, ListView):
    """Lista todos los estados de personas con búsqueda y filtrado"""
    model = Estado_Persona
    template_name = 'users/estado_persona_list.html'
    context_object_name = 'estados'
    paginate_by = 20

    def get_queryset(self):
        queryset = Estado_Persona.objects.all()
        search = self.request.GET.get('search')
        active = self.request.GET.get('active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        if active == 'true':
            queryset = queryset.filter(active=True)
        elif active == 'false':
            queryset = queryset.filter(active=False)
        
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['active_filter'] = self.request.GET.get('active', '')
        return context


class Estado_PersonaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un estado de persona"""
    model = Estado_Persona
    template_name = 'users/estado_persona_detail.html'
    context_object_name = 'estado'


class Estado_PersonaCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo estado de persona"""
    model = Estado_Persona
    form_class = Estado_PersonaForm
    template_name = 'users/estado_persona_form.html'
    success_url = reverse_lazy('estado-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Estado "{form.instance.name}" creado exitosamente.')
        return response


class Estado_PersonaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar estado de persona"""
    model = Estado_Persona
    form_class = Estado_PersonaForm
    template_name = 'users/estado_persona_form.html'
    success_url = reverse_lazy('estado-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Estado "{form.instance.name}" actualizado exitosamente.')
        return response


class Estado_PersonaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar estado de persona"""
    model = Estado_Persona
    template_name = 'users/estado_persona_confirm_delete.html'
    success_url = reverse_lazy('estado-list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Estado "{name}" eliminado exitosamente.')
        return response



# ==================== PERSONA VIEWS ====================

class PersonaListView(LoginRequiredMixin, ListView):
    """Lista todas las personas con búsqueda y filtrado"""
    model = Persona
    template_name = 'users/persona_list.html'
    context_object_name = 'personas'
    paginate_by = 20

    def get_queryset(self):
        queryset = Persona.objects.select_related('categoria_persona', 'cargo',
            'estado_persona', 'area'
        )
        q = self.request.GET.get('q', '').strip()
        active = self.request.GET.get('mostrar')
        area = self.request.GET.get('area')
        cargo = self.request.GET.get('cargo')
        
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(apellidos__icontains=q) |
                Q(identificador_interno__icontains=q) |
                Q(email__icontains=q)
            )
        
        if active == 'activas':
            queryset = queryset.filter(active=True)
        elif active == 'inactivas':
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


class PersonaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una persona"""
    model = Persona
    template_name = 'users/persona_detail.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        return context


class PersonaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva persona"""
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'
    success_url = reverse_lazy('persona-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        nombre_completo = f"{form.instance.nombre} {form.instance.apellidos}"
        messages.success(self.request, f'Persona "{nombre_completo}" creada exitosamente.')
        return response


class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar persona"""
    model = Persona
    form_class = PersonaForm
    template_name = 'users/persona_form.html'
    success_url = reverse_lazy('persona-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        nombre_completo = f"{form.instance.nombre} {form.instance.apellidos}"
        messages.success(self.request, f'Persona "{nombre_completo}" actualizada exitosamente.')
        return response


class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar persona"""
    model = Persona
    template_name = 'users/persona_confirm_delete.html'
    success_url = reverse_lazy('persona-list')

    def delete(self, request, *args, **kwargs):
        nombre_completo = f"{self.get_object().nombre} {self.get_object().apellidos}"
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Persona "{nombre_completo}" eliminada exitosamente.')
        return response


class PersonaConfigurarAreasView(LoginRequiredMixin, View):
    """Vista para que Alta Gerencia asigne áreas de supervisión a un usuario"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Alta Gerencia').exists():
            return redirect('acceso-denegado')
        return super().dispatch(request, *args, **kwargs)

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

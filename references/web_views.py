from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, 
    UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Departamento, Clasificacion_Sistema, Criticidad
from .forms import (
    DepartamentoForm,
    ClasificacionSistemaForm,
    CriticidadForm
)


# ============================================================================
# VISTAS WEB PARA DEPARTAMENTO
# ============================================================================

class DepartamentoListView(ListView):
    """Lista todos los departamentos"""
    model = Departamento
    template_name = 'references/departamento_list.html'
    context_object_name = 'departamentos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Departamento.objects.all()
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        # Filtro por estado activo
        active = self.request.GET.get('active')
        if active:
            queryset = queryset.filter(active=active == 'true')
        
        return queryset.order_by('name')


class DepartamentoDetailView(DetailView):
    """Detalle de un departamento específico"""
    model = Departamento
    template_name = 'references/departamento_detail.html'
    context_object_name = 'departamento'


class DepartamentoCreateView(CreateView):
    """Crear un nuevo departamento"""
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'references/departamento_form.html'
    success_url = reverse_lazy('departamento-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Departamento "{self.object.name}" creado exitosamente.')
        return response


class DepartamentoUpdateView(UpdateView):
    """Actualizar un departamento existente"""
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'references/departamento_form.html'
    success_url = reverse_lazy('departamento-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Departamento "{self.object.name}" actualizado exitosamente.')
        return response


class DepartamentoDeleteView(DeleteView):
    """Eliminar un departamento"""
    model = Departamento
    template_name = 'references/departamento_confirm_delete.html'
    success_url = reverse_lazy('departamento-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Departamento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# VISTAS WEB PARA CLASIFICACION_SISTEMA
# ============================================================================

class ClasificacionSistemaListView(ListView):
    """Lista todas las clasificaciones de sistemas"""
    model = Clasificacion_Sistema
    template_name = 'references/clasificacion_lista.html'
    context_object_name = 'clasificaciones'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Clasificacion_Sistema.objects.all()
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        # Filtro por estado activo
        active = self.request.GET.get('active')
        if active:
            queryset = queryset.filter(active=active == 'true')
        
        return queryset.order_by('name')


class ClasificacionSistemaDetailView(DetailView):
    """Detalle de una clasificación específica"""
    model = Clasificacion_Sistema
    template_name = 'references/clasificacion_detalle.html'
    context_object_name = 'clasificacion'


class ClasificacionSistemaCreateView(CreateView):
    """Crear una nueva clasificación"""
    model = Clasificacion_Sistema
    form_class = ClasificacionSistemaForm
    template_name = 'references/clasificacion_form.html'
    success_url = reverse_lazy('clasificacion-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Clasificación "{self.object.name}" creada exitosamente.')
        return response


class ClasificacionSistemaUpdateView(UpdateView):
    """Actualizar una clasificación existente"""
    model = Clasificacion_Sistema
    form_class = ClasificacionSistemaForm
    template_name = 'references/clasificacion_form.html'
    success_url = reverse_lazy('clasificacion-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Clasificación "{self.object.name}" actualizada exitosamente.')
        return response


class ClasificacionSistemaDeleteView(DeleteView):
    """Eliminar una clasificación"""
    model = Clasificacion_Sistema
    template_name = 'references/clasificacion_confirm_delete.html'
    success_url = reverse_lazy('clasificacion-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Clasificación eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# VISTAS WEB PARA CRITICIDAD
# ============================================================================

class CriticidadListView(ListView):
    """Lista todas las criticidades"""
    model = Criticidad
    template_name = 'references/criticidad_lista.html'
    context_object_name = 'criticidades'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Criticidad.objects.all()
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        # Filtro por estado activo
        active = self.request.GET.get('active')
        if active:
            queryset = queryset.filter(active=active == 'true')
        
        return queryset.order_by('name')


class CriticidadDetailView(DetailView):
    """Detalle de una criticidad específica"""
    model = Criticidad
    template_name = 'references/criticidad_detalle.html'
    context_object_name = 'criticidad'


class CriticidadCreateView(CreateView):
    """Crear una nueva criticidad"""
    model = Criticidad
    form_class = CriticidadForm
    template_name = 'references/criticidad_form.html'
    success_url = reverse_lazy('criticidad-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Criticidad "{self.object.name}" creada exitosamente.')
        return response


class CriticidadUpdateView(UpdateView):
    """Actualizar una criticidad existente"""
    model = Criticidad
    form_class = CriticidadForm
    template_name = 'references/criticidad_form.html'
    success_url = reverse_lazy('criticidad-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Criticidad "{self.object.name}" actualizada exitosamente.')
        return response


class CriticidadDeleteView(DeleteView):
    """Eliminar una criticidad"""
    model = Criticidad
    template_name = 'references/criticidad_confirm_delete.html'
    success_url = reverse_lazy('criticidad-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Criticidad eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

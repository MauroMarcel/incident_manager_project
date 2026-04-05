from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Incidente, Tipo_Incidente
from .forms import IncidenteForm, Tipo_IncidenteForm


# ==================== TIPO_INCIDENTE VIEWS ====================

class Tipo_IncidenteListView(LoginRequiredMixin, ListView):
    model = Tipo_Incidente
    template_name = 'incidents/tipo_incidente_list.html'
    context_object_name = 'tipos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Tipo_Incidente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        return queryset.order_by('name')


class Tipo_IncidenteCreateView(LoginRequiredMixin, CreateView):
    model = Tipo_Incidente
    form_class = Tipo_IncidenteForm
    template_name = 'incidents/tipo_incidente_form.html'
    success_url = reverse_lazy('tipo-incidente-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Tipo "{form.instance.name}" creado exitosamente.')
        return response


class Tipo_IncidenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Tipo_Incidente
    form_class = Tipo_IncidenteForm
    template_name = 'incidents/tipo_incidente_form.html'
    success_url = reverse_lazy('tipo-incidente-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Tipo "{form.instance.name}" actualizado exitosamente.')
        return response


class Tipo_IncidenteDeleteView(LoginRequiredMixin, DeleteView):
    model = Tipo_Incidente
    template_name = 'incidents/tipo_incidente_confirm_delete.html'
    success_url = reverse_lazy('tipo-incidente-list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Tipo "{name}" eliminado exitosamente.')
        return response


# ==================== INCIDENTE VIEWS ====================

class IncidenteListView(LoginRequiredMixin, ListView):
    model = Incidente
    template_name = 'incidents/incidente_list.html'
    context_object_name = 'incidentes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Incidente.objects.select_related(
            'tipo_incidente', 'reportado_por', 'asignado_a'
        )
        search = self.request.GET.get('search')
        estado = self.request.GET.get('estado')
        impacto = self.request.GET.get('impacto')

        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(codigo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
        if impacto:
            queryset = queryset.filter(impacto=impacto)

        return queryset.order_by('-fecha_reporte')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['estado_filter'] = self.request.GET.get('estado', '')
        context['impacto_filter'] = self.request.GET.get('impacto', '')
        context['estados'] = Incidente.ESTADOS
        context['impactos'] = Incidente.IMPACTO
        return context


class IncidenteDetailView(LoginRequiredMixin, DetailView):
    model = Incidente
    template_name = 'incidents/incidente_detail.html'
    context_object_name = 'incidente'


class IncidenteCreateView(LoginRequiredMixin, CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'incidents/incidente_form.html'
    success_url = reverse_lazy('incidente-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Incidente "{self.object.codigo}" creado exitosamente.')
        return response


class IncidenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'incidents/incidente_form.html'
    success_url = reverse_lazy('incidente-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Incidente "{self.object.codigo}" actualizado exitosamente.')
        return response


class IncidenteDeleteView(LoginRequiredMixin, DeleteView):
    model = Incidente
    template_name = 'incidents/incidente_confirm_delete.html'
    success_url = reverse_lazy('incidente-list')

    def delete(self, request, *args, **kwargs):
        codigo = self.get_object().codigo
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Incidente "{codigo}" eliminado exitosamente.')
        return response
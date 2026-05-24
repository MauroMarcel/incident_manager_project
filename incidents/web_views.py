from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Incidente
# from references.models import TipoIncidente


# ==================== TIPO_INCIDENTE VIEWS ====================

# ==================== INCIDENTE VIEWS ====================


    model = Incidente
    template_name = 'incidents/incidente_confirm_delete.html'
    success_url = reverse_lazy('incidente-list')

    def delete(self, request, *args, **kwargs):
        codigo = self.get_object().codigo
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Incidente "{codigo}" eliminado exitosamente.')
        return response
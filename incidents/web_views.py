from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import Incidente


class IncidenteDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Administrador', 'Supervisor']
        ).exists()

    def get(self, request, pk):
        incidente = get_object_or_404(Incidente, pk=pk, active=True)
        return render(request, 'incidents/incidente_confirm_delete.html', {
            'incidente': incidente
        })

    def post(self, request, pk):
        incidente = get_object_or_404(Incidente, pk=pk, active=True)
        incidente.active = False
        incidente.save()
        messages.success(request, f'Incidente "{incidente.codigo}" eliminado lógicamente.')
        return redirect('incidente-lista')

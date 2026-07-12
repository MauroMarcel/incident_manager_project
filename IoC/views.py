from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import IoC
from .forms import IoCForm
from base.mixins import RolRequeridoMixin
from .filters import IoCFilter


class IoCDetailView(RolRequeridoMixin,DetailView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Especialista']
    model = IoC
    template_name = 'IoC/ioc_detail.html'
    context_object_name = 'ioc'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class IoCCreateView(RolRequeridoMixin,CreateView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Especialista']
    model = IoC
    form_class = IoCForm
    template_name = 'IoC/ioc_form.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_success_url(self):
        return reverse_lazy('ioc-detalle', kwargs={'pk': self.object.pk})


class IoCUpdateView(RolRequeridoMixin, UpdateView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Especialista']
    model = IoC
    form_class = IoCForm
    template_name = 'IoC/ioc_form.html'
    context_object_name = 'ioc'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_success_url(self):
        return reverse_lazy('ioc-detalle', kwargs={'pk': self.object.pk})



class IoCListView(RolRequeridoMixin,ListView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Especialista']
    model = IoC
    template_name = 'IoC/ioc_list.html'
    context_object_name = 'iocs'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_queryset(self):
        queryset= IoC.objects.all()
        
        self.filterset = IoCFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

from django.views.generic import TemplateView
from base.mixins import RolRequeridoMixin 
from .models import Area
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import AreaForm 
from django import forms    

class AreaTreeView(RolRequeridoMixin, TemplateView):
    roles_permitidos = ['Administrador', 'Supervisor', 'Alta Gerencia']
    template_name = 'organizations/area_tree.html'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Solo las áreas raíz — sin área superior
        context['areas_raiz'] = Area.objects.filter(area_superior=None)
        return context
    


class AreaCreateView(RolRequeridoMixin, CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'organizations/area_form.html'
    roles_permitidos = ['Administrador'] 
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_success_url(self):
        # Redirige al árbol organizacional después de crear el área
        return reverse_lazy('area-tree')
    def get_initial(self):
        initial = super().get_initial()
        parent_pk = self.request.GET.get('parent')
        if parent_pk:
            initial['area_superior'] = parent_pk
        return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        parent_pk = self.request.GET.get('parent')
        if parent_pk:
            # Si viene con parent, ocultar el campo area_superior
            form.fields['area_superior'].widget = forms.HiddenInput()
        return form


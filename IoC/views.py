from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import IoC
from .forms import IoCForm

class IoCDetailView(DetailView):
    model = IoC
    template_name = 'IoC/ioc_detail.html'
    context_object_name = 'ioc'

class IoCCreateView(CreateView):
    model = IoC
    form_class = IoCForm
    template_name = 'IoC/ioc_form.html'

    # Redirige al detalle del IoC recién creado
    def get_success_url(self):
        return reverse_lazy('ioc-detalle', kwargs={'pk': self.object.pk})



class IoCListView(ListView):
    model = IoC
    template_name = 'IoC/ioc_list.html'
    context_object_name = 'iocs'

    def get_queryset(self):
        return IoC.objects.all()

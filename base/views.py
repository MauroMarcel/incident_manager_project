from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import TemplateView

class AccesoDenegadoView(TemplateView):
    template_name = 'base/acceso_denegado.html'

class HomeView(TemplateView):
    template_name = 'base/home.html'


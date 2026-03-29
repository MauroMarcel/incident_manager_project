from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    """Vista de inicio - página principal después del login"""
    template_name = 'home.html'
    login_url = 'login'

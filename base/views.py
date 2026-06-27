from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def csrf_failure(request, reason=""):
    return render(request, '403.html', status=403)


class AccesoDenegadoView(TemplateView):
    template_name = 'base/acceso_denegado.html'

class HomeView(TemplateView):
    template_name = 'base/home.html'


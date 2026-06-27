from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class RolRequeridoMixin(LoginRequiredMixin):
    roles_permitidos = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(
            name__in=self.roles_permitidos
        ).exists():
            return redirect('acceso-denegado')
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
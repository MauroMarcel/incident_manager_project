from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings


class IdleSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last = request.session.get('last_activity')
            now = timezone.now().timestamp()
            timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)
            if last and (now - last) > timeout:
                logout(request)
                return redirect(settings.LOGIN_URL)
            request.session['last_activity'] = now
        return self.get_response(request)

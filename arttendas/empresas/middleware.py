import threading
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = request.user

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'user'):
            del _thread_locals.user
        return response

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if not request.user.is_authenticated:
            allowed = ['/admin', getattr(settings, 'LOGIN_URL', '/accounts/login/'), '/empresas/cadastro', '/accounts/']
            if not any(path.startswith(p) for p in allowed):
                return redirect(f"/admin/login/?next={path}")

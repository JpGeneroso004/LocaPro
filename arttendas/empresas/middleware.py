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
            allowed = ['/admin', getattr(settings, 'LOGIN_URL', '/accounts/login/'), '/empresas/cadastro', '/accounts/', '/static/', '/media/']
            if not any(path.startswith(p) for p in allowed):
                return redirect(f"/accounts/login/?next={path}")

class BloqueioInadimplenteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'organizacao') and request.user.organizacao:
            path = request.path_info
            
            # Rotas permitidas mesmo se bloqueado
            allowed = [
                '/empresas/assinatura/', 
                '/admin/logout/', 
                '/accounts/logout/'
            ]
            
            if any(path.startswith(p) for p in allowed):
                return None
                
            # Se for superuser, não bloqueia (para suporte)
            if request.user.is_superuser:
                return None
                
            if request.user.organizacao.is_bloqueada:
                return redirect('empresas:assinatura')

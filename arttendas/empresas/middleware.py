import threading
import logging
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve

logger = logging.getLogger(__name__)

class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"Erro Crítico Capturado: {exception}", exc_info=True)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/'):
            return JsonResponse({'error': 'Erro interno do servidor. Nossa equipe já foi notificada.'}, status=500)
        return render(request, '500.html', status=500)

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        try:
            response = self.get_response(request)
            return response
        finally:
            if hasattr(_thread_locals, 'user'):
                del _thread_locals.user

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        
        # 1. Redireciona usuários não autenticados para o login
        if not request.user.is_authenticated:
            allowed = ['/admin', getattr(settings, 'LOGIN_URL', '/accounts/login/'), '/empresas/cadastro', '/empresas/webhook/asaas/', '/accounts/', '/static/', '/media/']
            if not any(path.startswith(p) for p in allowed):
                return redirect(f"/accounts/login/?next={path}")
                
        # 2. Usuário autenticado, mas SEM organização (ex: Logou pelo Google pela primeira vez)
        elif not getattr(request.user, 'organizacao_id', None) and not request.user.is_superuser:
            allowed_for_no_tenant = ['/empresas/cadastro', '/accounts/logout', '/static/', '/media/']
            if not any(path.startswith(p) for p in allowed_for_no_tenant):
                return redirect('empresas:cadastro')

class BloqueioInadimplenteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'organizacao') and request.user.organizacao:
            path = request.path_info
            
            # Rotas permitidas mesmo se bloqueado
            allowed = [
                '/empresas/assinatura/', 
                '/empresas/configuracoes/excluir/',
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

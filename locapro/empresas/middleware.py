import threading
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

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
    """
    Identifica o usuário logado e o injeta na ThreadLocal para ser consumido
    pelo TenantManager globalmente, isolando os dados (SaaS Multi-Tenant).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Injeta o usuário da requisição atual na memória local da thread
        _thread_locals.user = getattr(request, 'user', None)
        
        try:
            # 2. Processa a view
            response = self.get_response(request)
            return response
        finally:
            # 3. CRÍTICO: Limpa a memória SEMPRE (mesmo se der erro 500) 
            # para não vazar a sessão de um Tenant para outro na mesma Thread.
            _thread_locals.user = None

class BloqueioInadimplenteMiddleware:
    """
    Verifica se o usuário logado pertence a uma organização inadimplente.
    Se estiver inadimplente, bloqueia o acesso e redireciona para a página de assinatura.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'organizacao') and request.user.organizacao:
            org = request.user.organizacao
            
            if org.status_assinatura == 'inadimplente' and not request.user.is_superuser:
                # Exceção para não causar loop infinito em rotas cruciais
                allowed_paths = [
                    '/empresas/assinatura/',
                    '/empresas/webhook/asaas/',
                    '/accounts/logout/',
                    '/admin/logout/',
                    '/static/', # CRÍTICO: Sem isso, a página de pagamento carregava sem CSS
                    '/media/'
                ]
                
                path = request.path_info
                
                if not any(path.startswith(p) for p in allowed_paths):
                    messages.error(request, 'Sua assinatura está suspensa por inadimplência. Regularize para voltar a acessar o painel.')
                    return redirect('empresas:assinatura')
                    
        return self.get_response(request)

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        
        # 1. Redireciona usuários não autenticados para o login
        if not request.user.is_authenticated:
            allowed_prefixes = [
                '/admin', 
                getattr(settings, 'LOGIN_URL', '/accounts/login/'), 
                '/empresas/cadastro', 
                '/empresas/webhook/asaas/', 
                '/accounts/', 
                '/static/', 
                '/media/', 
                '/eventos/contrato/assinatura/',
                '/empresas/c/' # Vitrine pública
            ]
            
            # Permite exatamente a raiz (Landing Page) ou os prefixos liberados
            is_allowed = (path == '/') or any(path.startswith(p) for p in allowed_prefixes)
            
            if not is_allowed:
                return redirect(f"/accounts/login/?next={path}")
                
        # 2. Usuário autenticado, mas SEM organização (ex: Logou pelo Google pela primeira vez)
        elif not getattr(request.user, 'organizacao_id', None) and not request.user.is_superuser:
            allowed_for_no_tenant = ['/empresas/cadastro', '/accounts/logout', '/static/', '/media/']
            if not any(path.startswith(p) for p in allowed_for_no_tenant):
                return redirect('empresas:cadastro')

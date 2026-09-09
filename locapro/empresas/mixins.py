from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class TenantRequiredMixin(LoginRequiredMixin):
    """
    Garante que o usuário autenticado está devidamente vinculado a uma Organização.
    Se não estiver, o acesso às áreas internas do painel é bloqueado.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if not getattr(request.user, 'organizacao_id', None):
            raise PermissionDenied("Acesso Negado: Seu usuário não está vinculado a uma empresa ativa.")
            
        return super().dispatch(request, *args, **kwargs)

class TenantModelMixin:
    """
    Bloqueio de Injeção de ID (Segurança de Payload):
    Força que a gravação no banco de dados utilize a organizacao_id
    vinculada à sessão do usuário logado. Ignora totalmente
    qualquer parâmetro "organizacao" enviado maliciosamente por POST.
    """
    def form_valid(self, form):
        form.instance.organizacao = self.request.user.organizacao
        return super().form_valid(form)

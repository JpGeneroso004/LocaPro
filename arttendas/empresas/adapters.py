from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from empresas.models import Organizacao

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Se for um novo usuário vindo do Google, cria uma Organização para ele
        if not user.organizacao:
            # Pega o primeiro nome ou o inicio do email
            nome_base = user.first_name
            if not nome_base:
                nome_base = user.email.split('@')[0] if user.email else 'Usuário'
                
            org_nome = f"Locadora de {nome_base}"
            org = Organizacao.objects.create(nome=org_nome)
            user.organizacao = org
            user.save()
            
        return user

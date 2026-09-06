from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from empresas.models import Organizacao, Usuario
from datetime import timedelta

class Command(BaseCommand):
    help = "Varre locadoras inativas e envia avisos ou exclui as fantasmas (6 meses sem login)."

    def handle(self, *args, **kwargs):
        hoje = timezone.now()
        
        # Como iteramos por locadoras, precisamos ignorar locadoras recém-criadas sem usuários ainda
        locadoras = Organizacao.objects.all()
        
        for locadora in locadoras:
            # Pega o último login de qualquer usuário da locadora
            usuarios = Usuario.objects.filter(organizacao=locadora)
            if not usuarios.exists():
                continue
                
            # Verifica a data do login mais recente
            ultimo_login = usuarios.order_by("-last_login").first().last_login
            
            # Se ninguém logou e a conta foi criada há mais de 6 meses
            if not ultimo_login:
                continue
                
            # IMPORTANTE: Nunca deletar empresas que estão com a assinatura financeira ATIVA, mesmo que não acessem!
            if locadora.status_assinatura == 'ativa':
                continue
                
            dias_inativos = (hoje - ultimo_login).days
            
            # Dono da locadora para enviar o email
            dono = usuarios.filter(cargo="dono").first()
            if not dono:
                continue

            if dias_inativos == 165:
                # Faltam 15 dias para exclusão
                self.stdout.write(self.style.WARNING(f"Aviso enviado para {locadora.nome} (165 dias inativa)."))
                send_mail(
                    subject="[LocaPro] AVISO: Sua conta será excluída por inatividade",
                    message=f"Olá {dono.first_name},\n\nNotamos que sua locadora ({locadora.nome}) não tem acessos há mais de 5 meses.\n\nComo somos uma plataforma focada em empresas ativas, locadoras fantasmas são removidas após 6 meses de inatividade.\n\nPara evitar que sua conta e todos os seus dados sejam excluídos permanentemente em 15 dias, basta fazer login no sistema.\n\nAtenciosamente,\nEquipe LocaPro",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[dono.email],
                    fail_silently=True,
                )
            
            elif dias_inativos >= 180:
                # 6 meses cravados ou mais -> Hard Delete
                self.stdout.write(self.style.ERROR(f"Excluindo locadora fantasma: {locadora.nome} ({dias_inativos} dias)."))
                
                # Email de despedida
                send_mail(
                    subject="[LocaPro] Conta Excluída por Inatividade",
                    message=f"Olá {dono.first_name},\n\nSua locadora ({locadora.nome}) foi excluída permanentemente de nossa base de dados por exceder o limite de 6 meses de inatividade.\n\nAgradecemos o tempo que esteve conosco.\n\nEquipe LocaPro",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[dono.email],
                    fail_silently=True,
                )
                
                # Exclui a locadora e todos os dados em cascata (eventos, contratos, estoque)
                locadora.delete()
                # Exclui os usuários (para limpar o banco)
                usuarios.delete()

        self.stdout.write(self.style.SUCCESS("Varredura de fantasmas concluída com sucesso."))

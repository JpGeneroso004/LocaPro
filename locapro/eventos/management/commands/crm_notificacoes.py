from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from eventos.models import Evento
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Envia e-mails automáticos do CRM (Lembrete de Véspera e Pós-Evento)"

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        amanha = hoje + timedelta(days=1)
        ontem = hoje - timedelta(days=1)
        
        # 1. Lembrete de Véspera
        eventos_amanha = Evento.objects.filter(data_inicio=amanha, status="agendado").exclude(cliente_fidelidade=None)
        
        count_ida = 0
        for evento in eventos_amanha:
            cliente = evento.cliente_fidelidade
            if cliente and cliente.email:
                empresa = evento.organizacao.nome if evento.organizacao else "Nossa Locadora"
                assunto = f"Falta pouco! Sua estrutura da {empresa} chega amanhã!"
                mensagem = f"Olá {cliente.nome},\n\nEste é um lembrete automático de que a montagem da sua estrutura para o evento em {evento.cidade} está agendada para iniciar amanhã ({amanha.strftime('%d/%m/%Y')}).\n\nQualquer dúvida, estamos à disposição.\n\nAtenciosamente,\nEquipe {empresa}"
                
                try:
                    send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [cliente.email])
                    count_ida += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao enviar email para {cliente.email}: {str(e)}"))

        # 2. Pesquisa de Satisfação (Pós-Evento)
        eventos_ontem = Evento.objects.filter(data_fim=ontem, status="em_andamento").exclude(cliente_fidelidade=None)
        
        count_volta = 0
        for evento in eventos_ontem:
            cliente = evento.cliente_fidelidade
            if cliente and cliente.email:
                empresa = evento.organizacao.nome if evento.organizacao else "Nossa Locadora"
                assunto = f"Obrigado por escolher a {empresa}!"
                mensagem = f"Olá {cliente.nome},\n\nEsperamos que seu evento tenha sido um sucesso absoluto!\n\nAgradecemos a confiança em nossos materiais. Se puder, avalie nosso atendimento respondendo este e-mail.\n\nAté a próxima!\n\nAtenciosamente,\nEquipe {empresa}"
                
                try:
                    send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [cliente.email])
                    # Opcional: auto-marcar como concluído
                    evento.status = "concluido"
                    evento.save()
                    count_volta += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao enviar email pós-evento para {cliente.email}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"CRM Executado. Lembretes enviados: {count_ida}. Pesquisas enviadas: {count_volta}."))


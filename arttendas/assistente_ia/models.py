from django.db import models

class ConfiguracaoIA(models.Model):
    organizacao = models.OneToOneField('empresas.Organizacao', on_delete=models.CASCADE, related_name='config_ia')
    bot_ativo = models.BooleanField('Bot Ativo no WhatsApp', default=False)
    numero_whatsapp = models.CharField('Número Conectado', max_length=20, blank=True, help_text='Ex: 5561998542025')
    nome_assistente = models.CharField('Nome do Robô', max_length=50, default='LocaBot')
    prompt_personalidade = models.TextField('Personalidade e Regras (Prompt)', 
        default='Você é um assistente virtual de uma empresa de locação de tendas. Seja educado e focado em vendas.')
    
    # Configurações de API (Meta Graph API, OpenAI, etc)
    api_key_llm = models.CharField('Chave API da Inteligência (OpenAI/Gemini)', max_length=200, blank=True)
    webhook_token = models.CharField('Token de Validação do Webhook (WhatsApp)', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Configuração da Inteligência Artificial'
        verbose_name_plural = 'Configurações de IA'

    def __str__(self):
        return f"IA de {self.organizacao.nome}"

class MensagemWhatsApp(models.Model):
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE)
    telefone_cliente = models.CharField('Telefone do Cliente', max_length=20)
    mensagem = models.TextField('Conteúdo da Mensagem')
    is_bot = models.BooleanField('Enviado pelo Bot?', default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']


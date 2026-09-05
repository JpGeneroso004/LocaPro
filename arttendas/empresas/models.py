from django.db import models
from django.contrib.auth.models import AbstractUser

class Organizacao(models.Model):
    nome = models.CharField('Nome da Empresa', max_length=150)
    cnpj = models.CharField('CNPJ', max_length=20, blank=True)
    telefone = models.CharField('Telefone Principal', max_length=20, blank=True)
    logo = models.ImageField('Logo da Empresa', upload_to='logos/', null=True, blank=True)
    cor_primaria = models.CharField('Cor Principal', max_length=7, default='#004581', help_text='Cor tema da locadora')
    clausulas_padrao = models.TextField('Cláusulas Padrão do Contrato', blank=True, 
        default="1. RESPONSABILIDADE DO LOCAL: O Contratante é responsável por autorizações...\n2. FORÇA MAIOR: A Contratada isenta-se...")
    
    # Campos de SaaS (Assinatura)
    STATUS_ASSINATURA = [
        ('trial', 'Em Teste (Trial)'),
        ('ativa', 'Ativa'),
        ('inadimplente', 'Inadimplente (Bloqueada)'),
        ('cancelada', 'Cancelada'),
    ]
    status_assinatura = models.CharField('Status da Assinatura', max_length=15, choices=STATUS_ASSINATURA, default='trial')
    vencimento_trial = models.DateField('Vencimento do Trial', null=True, blank=True)
    asaas_customer_id = models.CharField('Asaas Customer ID', max_length=100, blank=True)
    asaas_subscription_id = models.CharField('Asaas Subscription ID', max_length=100, blank=True)
    
    # Configurações do LocaPoints (Fidelidade)
    fidelidade_ativa = models.BooleanField('Ativar LocaPoints', default=True)
    pontos_por_real = models.PositiveIntegerField('Quantos pontos o cliente ganha a cada R$ 1 pago?', default=1)
    taxa_resgate = models.PositiveIntegerField('Quantos pontos equivalem a R$ 1 de desconto?', default=100)
    
    # Indique e Ganhe (B2B Referral)
    codigo_indicacao = models.CharField('Código de Indicação', max_length=20, blank=True, unique=True, null=True)
    indicado_por = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='indicados')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        
    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.pk and not self.vencimento_trial:
            from django.utils import timezone
            import datetime
            self.vencimento_trial = timezone.localdate() + datetime.timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_bloqueada(self):
        from django.utils import timezone
        if self.status_assinatura == 'inadimplente' or self.status_assinatura == 'cancelada':
            return True
        if self.status_assinatura == 'trial' and self.vencimento_trial:
            if timezone.localdate() > self.vencimento_trial:
                return True
        return False

class Usuario(AbstractUser):
    CARGOS = [
        ('dono', 'Dono/Administrador'),
        ('funcionario', 'Funcionário')
    ]
    
    organizacao = models.ForeignKey(
        Organizacao, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )
    
    cargo = models.CharField('Cargo na Empresa', max_length=20, choices=CARGOS, default='dono')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class TenantManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        from .middleware import get_current_user
        user = get_current_user()
        
        # 1. Se não houver requisição (ex: terminal manage.py), retorna tudo.
        if user is None:
            return qs
            
        # 2. Se for uma requisição de um usuário não autenticado, não deve ver nada.
        if not user.is_authenticated:
            return qs.none()
            
        # 3. Se for Superuser, deixamos ver tudo (útil para o painel de admin).
        if user.is_superuser:
            return qs
            
        # 4. Se for usuário normal autenticado, filtra estritamente pela sua organização.
        if getattr(user, 'organizacao_id', None):
            return qs.filter(organizacao=user.organizacao)
            
        # 5. Segurança Final: Usuário logado mas sem organização (ex: logou pelo Google mas não criou locadora). NÃO DEVE VER NADA.
        return qs.none()

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify

class SoftDeleteModel(models.Model):
    deletado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.save(update_fields=['deletado_em'])

class Organizacao(SoftDeleteModel):
    slug = models.SlugField('Slug (URL Pública)', max_length=150, unique=True, blank=True)
    NICHOS = [
        ('tendas', 'Tendas e Estruturas'),
        ('som_luz', 'Som, Iluminação e Audiovisual'),
        ('brinquedos', 'Brinquedos Infláveis e Recreação'),
        ('mobiliario', 'Mobiliário (Mesas, Cadeiras, Louças)'),
        ('geradores', 'Geradores e Climatização'),
        ('multi', 'Multi-Segmento / Outros')
    ]
    
    nome = models.CharField('Nome da Empresa', max_length=150)
    segmento = models.CharField('Nicho de Mercado', max_length=20, choices=NICHOS, default='multi')
    cnpj = models.CharField('CNPJ', max_length=20, blank=True)
    telefone = models.CharField('Telefone Principal', max_length=20, blank=True)
    cidade = models.CharField('Cidade Sede', max_length=100, blank=True, help_text='Ex: São Paulo, Miami')
    estado = models.CharField('Estado/Província', max_length=50, blank=True)
    pais = models.CharField('País', max_length=50, default='Brasil')
    moeda = models.CharField('Moeda Base', max_length=10, default='BRL', help_text='BRL, USD, EUR...')
    chave_pix = models.CharField('Chave PIX (Recebimento)', max_length=100, blank=True, help_text='Se preenchida, aparecerá como QR Code/Chave nos contratos.')
    logo = models.ImageField('Logo da Empresa', upload_to='logos/', null=True, blank=True)
    cor_primaria = models.CharField('Cor Principal', max_length=7, default='#004581', help_text='Cor tema da locadora')
    clausulas_padrao = models.TextField('Cláusulas Padrão do Contrato', blank=True, default='1. RESPONSABILIDADE DO LOCAL: O Contratante é responsável por autorizações...\n2. FORÇA MAIOR: A Contratada isenta-se...')
    # Campos de SaaS (Assinatura)
    STATUS_ASSINATURA = [
        ('trial', 'Em Teste (Trial)'),
        ('ativa', 'Ativa'),
        ('inadimplente', 'Inadimplente'),
        ('cancelada', 'Cancelada'),
    ]
    
    PLANOS = [
        ('starter', 'Starter (Essencial)'),
        ('pro', 'Pro (Avançado)'),
        ('premium', 'Premium (Escala)'),
    ]

    # Plano e Assinatura
    plano = models.CharField('Plano Escolhido', max_length=20, choices=PLANOS, default='starter')
    ciclo_pagamento = models.CharField('Ciclo', max_length=10, default='MONTHLY')
    status_assinatura = models.CharField('Status da Assinatura', max_length=15, choices=STATUS_ASSINATURA, default='trial')
    vencimento_trial = models.DateField('Vencimento do Trial', null=True, blank=True)
    vencimento_assinatura = models.DateField('Próximo Vencimento', null=True, blank=True)
    
    # Integração Asaas
    asaas_customer_id = models.CharField('Asaas Customer ID', max_length=100, blank=True)
    asaas_subscription_id = models.CharField('Asaas Subscription ID', max_length=100, blank=True)
    
    # Gamificação / Fidelidade do SaaS (Níveis de Parceiro)
    meses_pagos = models.PositiveIntegerField('Meses de Assinatura Pagos', default=0)
    beneficio_ativo = models.CharField('Benefício de Longevidade', max_length=100, blank=True, help_text='Ex: Embaixador Prata (-5%)')
    
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
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            counter = 1
            while Organizacao.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if not self.pk and not self.vencimento_trial:
            self.vencimento_trial = timezone.localdate() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_bloqueada(self):
        if self.status_assinatura == 'inadimplente' or self.status_assinatura == 'cancelada':
            return True
        if self.status_assinatura == 'trial' and self.vencimento_trial:
            if timezone.localdate() > self.vencimento_trial:
                return True
        return False

class Usuario(AbstractUser, SoftDeleteModel):
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
        qs = super().get_queryset().filter(deletado_em__isnull=True)
        from .middleware import get_current_user
        user = get_current_user()
        
        if user is None:
            return qs
            
        if not user.is_authenticated:
            return qs.none()
            
        if user.is_superuser:
            return qs
            
        if getattr(user, 'organizacao_id', None):
            return qs.filter(organizacao=user.organizacao)
            
        return qs.none()

from django.db import models
from django.contrib.auth.models import AbstractUser

class Organizacao(models.Model):
    nome = models.CharField('Nome da Empresa', max_length=150)
    cnpj = models.CharField('CNPJ', max_length=20, blank=True)
    telefone = models.CharField('Telefone Principal', max_length=20, blank=True)
    logo = models.ImageField('Logo da Empresa', upload_to='logos/', null=True, blank=True)
    cor_primaria = models.CharField('Cor Principal', max_length=7, default='#FFD600', help_text='Cor tema da locadora')
    clausulas_padrao = models.TextField('Cláusulas Padrão do Contrato', blank=True, 
        default="1. RESPONSABILIDADE DO LOCAL: O Contratante é responsável por autorizações...\n2. FORÇA MAIOR: A Contratada isenta-se...")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        
    def __str__(self):
        return self.nome

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
        if user and user.is_authenticated and getattr(user, 'organizacao_id', None):
            return qs.filter(organizacao=user.organizacao)
        # Se for um comando de management (sem request), ou superuser sem tenant, retorna tudo.
        return qs

from django.db import models
from django.contrib.auth.models import AbstractUser

class Organizacao(models.Model):
    nome = models.CharField('Nome da Empresa', max_length=150)
    cnpj = models.CharField('CNPJ', max_length=20, blank=True)
    telefone = models.CharField('Telefone Principal', max_length=20, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        
    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    organizacao = models.ForeignKey(
        Organizacao, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

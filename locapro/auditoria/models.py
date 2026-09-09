from django.db import models
from empresas.models import Organizacao, Usuario, TenantManager

class LogAuditoria(models.Model):
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name='logs_auditoria')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    acao = models.CharField('Ação Executada', max_length=255)
    tabela_afetada = models.CharField('Tabela / Model', max_length=100)
    registro_id = models.IntegerField('ID do Registro', null=True, blank=True)
    detalhes = models.TextField('Detalhes da Alteração', blank=True)
    
    data_hora = models.DateTimeField('Data e Hora', auto_now_add=True)

    objects = TenantManager()

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-data_hora']

    def __str__(self):
        usuario_nome = self.usuario.email if self.usuario else "Sistema"
        return f"{self.data_hora.strftime('%d/%m/%Y %H:%M')} - {usuario_nome}: {self.acao}"

from django.db import models
from inventario.models import Tenda, ConjuntoPalco


class Evento(models.Model):
    STATUS = [
        ('agendado',     'Agendado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido',    'Concluído'),
        ('cancelado',    'Cancelado'),
    ]

    nome       = models.CharField('Nome do Evento', max_length=200)
    cliente    = models.CharField('Cliente / Responsável', max_length=200)
    telefone   = models.CharField('Telefone', max_length=20, blank=True)
    rua        = models.CharField('Rua', max_length=200, default='')
    numero     = models.CharField('Número', max_length=20, default='')
    setor      = models.CharField('Setor/Bairro', max_length=100, default='')
    complemento= models.CharField('Complemento', max_length=150, blank=True)
    cidade     = models.CharField('Cidade', max_length=100, default='Formosa')
    latitude   = models.DecimalField('Latitude',  max_digits=10, decimal_places=7, null=True, blank=True)
    longitude  = models.DecimalField('Longitude', max_digits=10, decimal_places=7, null=True, blank=True)
    data_inicio = models.DateField('Data de Início')
    hora_inicio = models.TimeField('Horário de Início', null=True, blank=True)
    data_fim    = models.DateField('Data de Fim')
    hora_fim    = models.TimeField('Horário de Fim', null=True, blank=True)
    status      = models.CharField('Status', max_length=20, choices=STATUS, default='agendado')
    observacoes = models.TextField('Observações', blank=True)
    tendas      = models.ManyToManyField(Tenda, blank=True, verbose_name='Tendas', related_name='eventos')
    conjuntos   = models.ManyToManyField(ConjuntoPalco, blank=True,
                                         verbose_name='Conjuntos de Palco/Piso', related_name='eventos')
    criado_em   = models.DateTimeField(auto_now_add=True)
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='eventos', null=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio']

    def __str__(self):
        return f'{self.nome} – {self.data_inicio}'

    def get_status_class(self):
        return {
            'agendado':     'badge-agendado',
            'em_andamento': 'badge-andamento',
            'concluido':    'badge-concluido',
            'cancelado':    'badge-cancelado',
        }.get(self.status, '')

    def total_tendas(self):
        return self.tendas.count()

    def total_placas(self):
        return sum(c.quantidade_placas for c in self.conjuntos.all())


class Contrato(models.Model):
    evento = models.OneToOneField(Evento, on_delete=models.CASCADE, related_name='contrato', verbose_name='Evento')
    
    # Dados do Contratante
    contratante_nome = models.CharField('Nome', max_length=200)
    contratante_cpf_cnpj = models.CharField('CPF/CNPJ', max_length=30)
    contratante_telefone = models.CharField('Telefone', max_length=20)
    contratante_endereco = models.CharField('Endereço', max_length=300)
    
    # Dados da Locação
    data_montagem = models.DateTimeField('Data/Hora Montagem', null=True, blank=True)
    data_desmontagem = models.DateTimeField('Data/Hora Desmontagem', null=True, blank=True)
    endereco_montagem = models.CharField('Endereço da Montagem', max_length=300)
    
    # Valores e Pagamento
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2, default=0.00)
    sinal = models.DecimalField('Sinal', max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=100)
    
    # Itens (Texto para o contrato, pode ser gerado automaticamente e editado)
    itens_locados = models.TextField('Itens Locados')
    
    # Cláusulas e Observações (Texto completo para ser editável)
    clausulas = models.TextField('Cláusulas')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f"Contrato - {self.evento.nome}"
        
    @property
    def saldo_restante(self):
        sinal_val = self.sinal if self.sinal else 0
        return self.valor_total - sinal_val

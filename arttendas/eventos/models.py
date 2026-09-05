from django.db import models
from inventario.models import Tenda, ConjuntoPalco
from empresas.models import TenantManager


class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=200)
    email = models.EmailField('E-mail do Cliente', blank=True, help_text='Necessário para avisos automáticos e envio de contratos')
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=30, blank=True)
    locapoints = models.PositiveIntegerField('LocaPoints Acumulados', default=0)
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='clientes')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    objects = TenantManager()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.locapoints} pts"

class Evento(models.Model):
    STATUS = [
        ('agendado',     'Agendado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido',    'Concluído'),
        ('cancelado',    'Cancelado'),
    ]

    nome       = models.CharField('Nome do Evento', max_length=200)
    cliente_fidelidade = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos', verbose_name='Cliente (Sistema Fidelidade)')
    cliente    = models.CharField('Cliente / Responsável (Legado)', max_length=200, blank=True)
    telefone   = models.CharField('Telefone', max_length=20, blank=True)
    rua        = models.CharField('Rua', max_length=200, default='')
    numero     = models.CharField('Número', max_length=20, default='')
    setor      = models.CharField('Setor/Bairro', max_length=100, default='')
    complemento= models.CharField('Complemento', max_length=150, blank=True)
    cidade     = models.CharField('Cidade', max_length=100, blank=True)
    latitude   = models.DecimalField('Latitude',  max_digits=10, decimal_places=7, null=True, blank=True)
    longitude  = models.DecimalField('Longitude', max_digits=10, decimal_places=7, null=True, blank=True)
    data_inicio = models.DateField('Data de Início', db_index=True)
    hora_inicio = models.TimeField('Horário de Início', null=True, blank=True)
    data_fim    = models.DateField('Data de Fim', db_index=True)
    hora_fim    = models.TimeField('Horário de Fim', null=True, blank=True)
    status      = models.CharField('Status', max_length=20, choices=STATUS, default='agendado', db_index=True)
    observacoes = models.TextField('Observações', blank=True)
    tendas      = models.ManyToManyField(Tenda, blank=True, verbose_name='Tendas', related_name='eventos')
    conjuntos   = models.ManyToManyField(ConjuntoPalco, blank=True,
                                         verbose_name='Conjuntos de Palco/Piso', related_name='eventos')
    criado_em   = models.DateTimeField(auto_now_add=True)
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='eventos')

    objects = TenantManager()

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
    valor_total = models.DecimalField('Valor Total (Base)', max_digits=10, decimal_places=2, default=0.00)
    sinal = models.DecimalField('Sinal', max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=100)
    
    # Fidelidade (LocaPoints)
    pontos_utilizados = models.PositiveIntegerField('Pontos Utilizados (Desconto)', default=0)
    desconto_fidelidade = models.DecimalField('Desconto Fidelidade (R$)', max_digits=10, decimal_places=2, default=0.00)
    pontos_gerados = models.PositiveIntegerField('Pontos Gerados (Para o futuro)', default=0)
    pontos_creditados = models.BooleanField('Pontos já creditados na carteira?', default=False)
    
    # Itens e Cláusulas
    itens_locados = models.TextField('Itens Locados')
    clausulas = models.TextField('Cláusulas')

    # Assinatura Eletrônica (SaaS)
    status_assinatura = models.CharField(
        'Status da Assinatura', 
        max_length=20, 
        choices=[('pendente', 'Pendente'), ('assinado', 'Assinado'), ('recusado', 'Recusado')],
        default='pendente'
    )
    data_assinatura = models.DateTimeField('Data da Assinatura', null=True, blank=True)
    ip_assinatura = models.GenericIPAddressField('IP da Assinatura', null=True, blank=True)
    token_assinatura = models.CharField('Token Seguro de Assinatura', max_length=100, unique=True, null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='contratos')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f"Contrato - {self.evento.nome}"
        
    @property
    def valor_final(self):
        return self.valor_total - self.desconto_fidelidade

    @property
    def saldo_restante(self):
        sinal_val = self.sinal if self.sinal else 0
        return self.valor_final - sinal_val

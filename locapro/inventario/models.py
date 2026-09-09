from django.db import models
from empresas.models import TenantManager, SoftDeleteModel, Organizacao
from django.db.models.signals import post_save
from django.dispatch import receiver

class CategoriaEquipamento(SoftDeleteModel):
    nome = models.CharField('Nome da Categoria', max_length=50)
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='categorias')
    
    objects = TenantManager()

    class Meta:
        verbose_name = 'Categoria de Equipamento'
        verbose_name_plural = 'Categorias de Equipamentos'
        ordering = ['nome']
        unique_together = ('nome', 'organizacao')

    def __str__(self):
        return self.nome

class Equipamento(SoftDeleteModel):
    STATUS = [
        ('ativo', 'Ativo (Disponível)'),
        ('inativo', 'Inativo / Manutenção'),
    ]
    TIPO_RASTREAMENTO = [
        ('lote', 'Por Lote (Quantidade)'),
        ('serializado', 'Único/Serializado (Patrimônio)'),
    ]

    codigo = models.CharField('Código (Opcional)', max_length=30, blank=True, help_text='Ex: CAIXA-01, MESA-PLAST')
    nome = models.CharField('Nome do Item', max_length=150, help_text='Ex: Cadeira de Plástico, Tenda Piramidal 5x5')
    categoria = models.ForeignKey(CategoriaEquipamento, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_rastreamento = models.CharField('Tipo de Controle', max_length=20, choices=TIPO_RASTREAMENTO, default='lote')
    quantidade_lote = models.PositiveIntegerField('Quantidade em Lote', default=1, help_text='Usado apenas se for rastreado por Lote')
    
    valor_diaria = models.DecimalField('Valor da Diária Base (R$)', max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField('Status', max_length=20, choices=STATUS, default='ativo')
    observacoes = models.TextField('Observações', blank=True)
    
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='equipamentos')
    
    objects = TenantManager()

    class Meta:
        verbose_name = 'Equipamento / Item'
        verbose_name_plural = 'Equipamentos / Itens'
        ordering = ['nome']

    def __str__(self):
        if self.tipo_rastreamento == 'lote':
            return f"{self.nome} (Qtd: {self.quantidade_lote})"
        return f"{self.nome} (Serializado)"

    def get_status_class(self):
        return {
            'ativo': 'status-disponivel',
            'inativo': 'status-manutencao',
        }.get(self.status, '')

    def save(self, *args, **kwargs):
        if not self.codigo:
            from django.utils.text import slugify
            base = slugify(self.nome)[:6].upper()
            count = Equipamento.objects.filter(organizacao=self.organizacao).count() + 1
            self.codigo = f"{base}-{count:03d}"
        super().save(*args, **kwargs)

class Patrimonio(SoftDeleteModel):
    STATUS_PATRIMONIO = [
        ('disponivel', 'Disponível'),
        ('em_manutencao', 'Em Manutenção'),
        ('inativo', 'Inativo / Danificado'),
    ]
    
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='patrimonios')
    numero_serie_ou_tag = models.CharField('Número de Série / Tag ID', max_length=100)
    status = models.CharField('Status', max_length=20, choices=STATUS_PATRIMONIO, default='disponivel')
    
    organizacao = models.ForeignKey('empresas.Organizacao', on_delete=models.CASCADE, related_name='patrimonios')
    
    objects = TenantManager()

    class Meta:
        verbose_name = 'Patrimônio (Item Único)'
        verbose_name_plural = 'Patrimônios'

    def __str__(self):
        return f"{self.equipamento.nome} - {self.numero_serie_ou_tag}"

@receiver(post_save, sender='empresas.Organizacao')
def criar_categorias_iniciais(sender, instance, created, **kwargs):
    if created:
        categorias = []
        nicho = instance.segmento
        if nicho == 'tendas':
            categorias = ['Tendas Piramidais', 'Tendas Chapéu de Bruxa', 'Palcos e Pisos', 'Gradis']
        elif nicho == 'som_luz':
            categorias = ['Caixas de Som (P.A)', 'Microfones', 'Mesas de Som', 'Canhões de Luz (LED)', 'Máquinas de Fumaça']
        elif nicho == 'brinquedos':
            categorias = ['Camas Elásticas', 'Brinquedos Infláveis', 'Piscina de Bolinhas', 'Máquinas de Algodão Doce']
        elif nicho == 'mobiliario':
            categorias = ['Mesas de Plástico', 'Mesas Rústicas (Madeira)', 'Cadeiras', 'Toalhas e Capas', 'Louças e Talheres']
        elif nicho == 'geradores':
            categorias = ['Geradores a Diesel', 'Cabos e Extensões', 'Quadros de Distribuição']
        else:
            categorias = ['Equipamentos Principais', 'Acessórios', 'Estruturas']
            
        for cat in categorias:
            CategoriaEquipamento.objects.get_or_create(nome=cat, organizacao=instance)

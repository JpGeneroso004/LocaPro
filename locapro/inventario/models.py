from django.db import models
from empresas.models import TenantManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class CategoriaEquipamento(models.Model):
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

class Equipamento(models.Model):
    STATUS = [
        ('ativo', 'Ativo (Disponível)'),
        ('inativo', 'Inativo / Manutenção'),
    ]

    codigo = models.CharField('Código (Opcional)', max_length=30, blank=True, help_text='Ex: CAIXA-01, MESA-PLAST')
    nome = models.CharField('Nome do Item', max_length=150, help_text='Ex: Cadeira de Plástico, Tenda Piramidal 5x5, Pula-pula de Castelo')
    categoria = models.ForeignKey(CategoriaEquipamento, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Ao invés de criar 500 linhas para 500 cadeiras, criamos 1 linha com quantidade = 500
    quantidade_total = models.PositiveIntegerField('Quantidade em Estoque', default=1)
    
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
        return f"{self.nome} (Qtd: {self.quantidade_total})"

    def get_status_class(self):
        return {
            'ativo': 'status-disponivel',
            'inativo': 'status-manutencao',
        }.get(self.status, '')

    def save(self, *args, **kwargs):
        # Auto-gerar código se vazio (facilita pro cliente)
        if not self.codigo:
            from django.utils.text import slugify
            base = slugify(self.nome)[:6].upper()
            count = Equipamento.objects.filter(organizacao=self.organizacao).count() + 1
            self.codigo = f"{base}-{count:03d}"
        super().save(*args, **kwargs)


@receiver(post_save, sender='empresas.Organizacao')
def criar_categorias_iniciais(sender, instance, created, **kwargs):
    """
    Quando uma nova empresa se cadastra no SaaS, lemos o 'Nicho de Mercado' dela
    e populamos o banco de dados com as Categorias de Estoque mais comuns para aquele nicho.
    Isso cria um efeito "Uau" de Onboarding (Software Inteligente).
    """
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

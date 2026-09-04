from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def gerar_codigo_tenda():
    """Gera automaticamente o próximo código disponível: T-001, T-002..."""
    ultimo = Tenda.objects.order_by('-id').first()
    if not ultimo:
        return 'T-001'
    # Pega todos os códigos numéricos existentes
    codigos = []
    for t in Tenda.objects.all():
        try:
            num = int(t.codigo.replace('T-', ''))
            codigos.append(num)
        except ValueError:
            pass
    proximo = max(codigos) + 1 if codigos else 1
    return f'T-{proximo:03d}'


class Tenda(models.Model):
    TAMANHOS = [
        ('3x3',   '3x3 m'),
        ('4x4',   '4x4 m'),
        ('5x5',   '5x5 m'),
        ('6x6',   '6x6 m'),
        ('7x7',   '7x7 m'),
        ('8x8',   '8x8 m'),
        ('10x10', '10x10 m'),
    ]

    TIPOS = [
        ('piramidal',    'Piramidal'),
        ('chapeu_bruxa', 'Chapéu de Bruxa'),
    ]

    STATUS = [
        ('ativo', 'Ativo'),
        ('manutencao', 'Em Manutenção'),
    ]

    codigo    = models.CharField('Código', max_length=20, unique=True)
    tamanho   = models.CharField('Tamanho', max_length=10, choices=TAMANHOS)
    tipo      = models.CharField('Tipo', max_length=20, choices=TIPOS, default='piramidal')
    status    = models.CharField('Status', max_length=20, choices=STATUS, default='ativo')
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Tenda'
        verbose_name_plural = 'Tendas'
        ordering = ['tamanho', 'tipo', 'codigo']

    def __str__(self):
        return f'{self.codigo} – {self.get_tamanho_display()} {self.get_tipo_display()}'

    def get_status_class(self):
        return {
            'ativo': 'status-disponivel',
            'manutencao': 'status-manutencao',
        }.get(self.status, '')

    def save(self, *args, **kwargs):
        # Gera código automático se não informado
        if not self.codigo:
            self.codigo = gerar_codigo_tenda()
        super().save(*args, **kwargs)


class ConjuntoPalco(models.Model):
    """
    Um conjunto de palco/piso é formado por N placas.
    Exemplo: 'Palco Grande' com 20 placas.
    """
    STATUS = [
        ('ativo', 'Ativo'),
        ('manutencao', 'Em Manutenção'),
    ]

    nome             = models.CharField('Nome do Conjunto', max_length=100)
    quantidade_placas = models.PositiveIntegerField(
        'Número de Placas',
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        help_text='Quantas placas formam este conjunto (máx. 30)'
    )
    status      = models.CharField('Status', max_length=20, choices=STATUS, default='ativo')
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Conjunto de Palco/Piso'
        verbose_name_plural = 'Conjuntos de Palco/Piso'
        ordering = ['quantidade_placas']

    def __str__(self):
        return self.nome

    def get_status_class(self):
        return {
            'ativo': 'status-disponivel',
            'manutencao': 'status-manutencao',
        }.get(self.status, '')

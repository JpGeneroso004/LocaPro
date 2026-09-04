import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventario.models import Tenda, ConjuntoPalco

# Add Tenda 10x10
Tenda.objects.get_or_create(
    tamanho='10x10',
    tipo='piramidal',
    defaults={
        'codigo': 'T10X10-001',
        'status': 'disponivel'
    }
)

# Add Conjunto 30 placas
ConjuntoPalco.objects.get_or_create(
    nome='Conjunto Palco/Piso 30 Placas',
    defaults={
        'quantidade_placas': 30,
        'status': 'disponivel'
    }
)
print("Items added successfully.")

from django.apps import AppConfig

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'
    verbose_name = 'Inventário'

    def ready(self):
        try:
            from django.db import connection
            if 'inventario_tenda' not in connection.introspection.table_names():
                return
            from inventario.models import Tenda
            if Tenda.objects.exists():
                return
            tendas = [
                ('T-001','10x10','piramidal'),
                ('T-002','8x8','piramidal'),('T-003','8x8','piramidal'),
                ('T-004','7x7','chapeu_bruxa'),
                ('T-005','6x6','piramidal'),('T-006','6x6','piramidal'),
                ('T-007','6x6','piramidal'),('T-008','6x6','piramidal'),
                ('T-009','6x6','chapeu_bruxa'),('T-010','6x6','chapeu_bruxa'),
                ('T-011','5x5','piramidal'),('T-012','5x5','piramidal'),('T-013','5x5','piramidal'),
                ('T-014','4x4','piramidal'),('T-015','4x4','piramidal'),
                ('T-016','4x4','piramidal'),('T-017','4x4','piramidal'),
                ('T-018','4x4','chapeu_bruxa'),('T-019','4x4','chapeu_bruxa'),
                ('T-020','3x3','piramidal'),('T-021','3x3','piramidal'),
            ]
            for codigo, tamanho, tipo in tendas:
                Tenda.objects.get_or_create(codigo=codigo, defaults={
                    'tamanho': tamanho, 'tipo': tipo, 'status': 'disponivel'
                })

            from inventario.models import ConjuntoPalco
            if not ConjuntoPalco.objects.exists():
                for qtd in range(1, 31):
                    ConjuntoPalco.objects.get_or_create(
                        quantidade_placas=qtd,
                        defaults={'nome': f'Conjunto {qtd}', 'status': 'disponivel'}
                    )
        except Exception:
            pass

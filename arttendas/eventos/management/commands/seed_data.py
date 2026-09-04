from django.core.management.base import BaseCommand
from inventario.models import Tenda, ConjuntoPalco
from eventos.models import Evento
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstração'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Criando dados de demonstração...')

        # ── Tendas ────────────────────────────────────────────
        tendas_data = [
            ('T-001','10x10','piramidal'),
            ('T-002','8x8','piramidal'), ('T-003','8x8','piramidal'),
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
        for codigo, tamanho, tipo in tendas_data:
            Tenda.objects.get_or_create(codigo=codigo, defaults={
                'tamanho': tamanho, 'tipo': tipo, 'status': 'disponivel'
            })
        self.stdout.write(f'  ✅ {len(tendas_data)} tendas')

        # ── Conjuntos de Palco/Piso — 1 a 30 placas ──────────
        criados = 0
        for qtd in range(1, 31):
            _, novo = ConjuntoPalco.objects.get_or_create(
                quantidade_placas=qtd,
                defaults={'nome': f'Conjunto {qtd}', 'status': 'disponivel'}
            )
            if novo:
                criados += 1

        self.stdout.write(f'  ✅ {criados} conjuntos de palco/piso criados (1 a 30 placas)')

        # ── Eventos de demonstração ───────────────────────────
        hoje = date.today()
        eventos_data = [
            {
                'nome': 'Festa Junina Municipal',
                'cliente': 'Prefeitura de Formosa',
                'telefone': '(61) 3631-0000',
                'local': 'Praça do Coreto, Centro',
                'cidade': 'Formosa',
                'latitude': -15.5362, 'longitude': -47.3344,
                'data_inicio': hoje - timedelta(days=2),
                'data_fim': hoje + timedelta(days=1),
                'status': 'em_andamento',
                'observacoes': 'Evento de grande porte.',
                'tendas_ids': ['T-001','T-005','T-006'],
                'conjuntos_placas': [20],
            },
            {
                'nome': 'Casamento Silva & Santos',
                'cliente': 'Família Silva',
                'telefone': '(61) 99876-5432',
                'local': 'Sítio Recanto das Flores',
                'cidade': 'Formosa',
                'latitude': -15.5100, 'longitude': -47.3800,
                'data_inicio': hoje + timedelta(days=5),
                'data_fim': hoje + timedelta(days=5),
                'status': 'agendado',
                'observacoes': 'Entrega um dia antes.',
                'tendas_ids': ['T-011','T-012'],
                'conjuntos_placas': [10],
            },
            {
                'nome': 'Expo Agropecuária',
                'cliente': 'Sindicato Rural de Formosa',
                'telefone': '(61) 3631-1234',
                'local': 'Parque de Exposições, BR-020',
                'cidade': 'Formosa',
                'latitude': -15.5600, 'longitude': -47.3200,
                'data_inicio': hoje + timedelta(days=15),
                'data_fim': hoje + timedelta(days=19),
                'status': 'agendado',
                'observacoes': 'Evento de 5 dias.',
                'tendas_ids': ['T-002','T-003','T-004'],
                'conjuntos_placas': [],
            },
            {
                'nome': 'Show Gospel Renovar',
                'cliente': 'Igreja Renovar',
                'telefone': '(61) 98765-4321',
                'local': 'Avenida Brasil, 1200',
                'cidade': 'Formosa',
                'latitude': -15.5280, 'longitude': -47.3390,
                'data_inicio': hoje - timedelta(days=30),
                'data_fim': hoje - timedelta(days=30),
                'status': 'concluido',
                'observacoes': 'Realizado com sucesso.',
                'tendas_ids': [],
                'conjuntos_placas': [],
            },
        ]

        for ev_data in eventos_data:
            tendas_ids      = ev_data.pop('tendas_ids')
            conjuntos_placas = ev_data.pop('conjuntos_placas')
            ev, criado = Evento.objects.get_or_create(nome=ev_data['nome'], defaults=ev_data)
            if criado:
                for cod in tendas_ids:
                    try: ev.tendas.add(Tenda.objects.get(codigo=cod))
                    except Tenda.DoesNotExist: pass
                for qtd in conjuntos_placas:
                    try: ev.conjuntos.add(ConjuntoPalco.objects.get(quantidade_placas=qtd))
                    except ConjuntoPalco.DoesNotExist: pass
                if ev.status in ['agendado', 'em_andamento']:
                    ev.tendas.all().update(status='em_uso')
                    ev.conjuntos.all().update(status='em_uso')

        self.stdout.write('  ✅ 4 eventos de demonstração')
        self.stdout.write(self.style.SUCCESS('\n🎉 Tudo pronto!\n'))

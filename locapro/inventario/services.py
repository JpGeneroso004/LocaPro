from django.db import transaction
from django.db.models import Sum
from inventario.models import Equipamento, Patrimonio
from eventos.models import Evento, ItemEvento

class EstoqueIndisponivelError(Exception):
    pass

def verificar_disponibilidade(equipamento_id, data_inicio, data_fim, quantidade_desejada=1):
    """
    Motor de Cálculo de Disponibilidade.
    Verifica se há estoque para um equipamento nas datas solicitadas (Fase Front-end/Visualização).
    """
    equipamento = Equipamento.objects.get(id=equipamento_id)
    
    # 1. Filtra eventos concorrentes: que estejam Agendados ou Em Andamento
    # e que colidam com a janela de tempo solicitada.
    eventos_concorrentes = Evento.objects.filter(
        status__in=['agendado', 'em_andamento'],
        data_inicio__lte=data_fim,
        data_fim__gte=data_inicio
    )
    
    if equipamento.tipo_rastreamento == 'lote':
        # Cálculo para Lote: Soma as quantidades deste item alocadas nos eventos concorrentes
        itens_alocados = ItemEvento.objects.filter(
            equipamento=equipamento, 
            evento__in=eventos_concorrentes
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        
        disponivel = equipamento.quantidade_lote - itens_alocados
        return disponivel >= quantidade_desejada, disponivel
        
    elif equipamento.tipo_rastreamento == 'serializado':
        # Cálculo para Serial: Lista os IDs dos patrimônios já alocados no período
        patrimonios_alocados_ids = ItemEvento.objects.filter(
            equipamento=equipamento,
            evento__in=eventos_concorrentes,
            patrimonio__isnull=False
        ).values_list('patrimonio_id', flat=True)
        
        # Filtra os patrimônios vivos (disponíveis para aluguel e que não estão na lista acima)
        # Note que se o patrimônio estiver "em_manutencao", ele será ignorado aqui.
        patrimonios_livres = Patrimonio.objects.filter(
            equipamento=equipamento,
            status='disponivel'
        ).exclude(id__in=patrimonios_alocados_ids)
        
        total_livre = patrimonios_livres.count()
        return total_livre >= quantidade_desejada, total_livre

@transaction.atomic
def alocar_itens_evento(evento, itens_solicitados):
    """
    Motor Transacional Definitivo de Reserva (Fase Checkout).
    itens_solicitados: list of dicts [{'equipamento_id': 1, 'quantidade': 2}]
    Utiliza select_for_update() para criar um lock no banco e erradicar OVERBOOKING.
    """
    for item in itens_solicitados:
        equipamento_id = item['equipamento_id']
        qtd_solicitada = item['quantidade']
        
        # LOCK DE CONCORRÊNCIA: Se dois clientes clicarem em "Fechar Contrato" no mesmo milissegundo,
        # o banco de dados forçará um deles a esperar nesta linha.
        equipamento = Equipamento.objects.select_for_update().get(id=equipamento_id)
        
        # Após obter exclusividade do dado, fazemos a checagem real
        tem_dispo, qtd_dispo = verificar_disponibilidade(
            equipamento_id=equipamento.id,
            data_inicio=evento.data_inicio,
            data_fim=evento.data_fim,
            quantidade_desejada=qtd_solicitada
        )
        
        if not tem_dispo:
            raise EstoqueIndisponivelError(f"Estoque insuficiente para {equipamento.nome}. Apenas {qtd_dispo} disponíveis.")
        
        # Criação do vínculo no banco
        if equipamento.tipo_rastreamento == 'lote':
            ItemEvento.objects.create(
                evento=evento,
                equipamento=equipamento,
                quantidade=qtd_solicitada,
                organizacao=evento.organizacao,
                preco_fechado=equipamento.valor_diaria * qtd_solicitada
            )
            
        elif equipamento.tipo_rastreamento == 'serializado':
            # Para itens seriais, aplicamos LOCK também nos registros dos patrimônios,
            # pegando os N primeiros livres.
            eventos_concorrentes = Evento.objects.filter(
                status__in=['agendado', 'em_andamento'],
                data_inicio__lte=evento.data_fim,
                data_fim__gte=evento.data_inicio
            )
            
            patrimonios_alocados_ids = ItemEvento.objects.filter(
                equipamento=equipamento,
                evento__in=eventos_concorrentes,
                patrimonio__isnull=False
            ).values_list('patrimonio_id', flat=True)
            
            # O [:qtd_solicitada] junto com select_for_update garante que estamos
            # prendendo exatamente as máquinas físicas que o cliente vai levar
            patrimonios_livres = Patrimonio.objects.select_for_update().filter(
                equipamento=equipamento,
                status='disponivel'
            ).exclude(id__in=patrimonios_alocados_ids)[:qtd_solicitada]
            
            if len(patrimonios_livres) < qtd_solicitada:
                raise EstoqueIndisponivelError(f"Concorrência: Unidades de {equipamento.nome} foram alugadas por outro usuário no último segundo.")
            
            # Para controle serial, criamos 1 ItemEvento com quantidade=1 para CADA patrimônio
            for patrimonio in patrimonios_livres:
                ItemEvento.objects.create(
                    evento=evento,
                    equipamento=equipamento,
                    patrimonio=patrimonio,
                    quantidade=1,
                    organizacao=evento.organizacao,
                    preco_fechado=equipamento.valor_diaria
                )

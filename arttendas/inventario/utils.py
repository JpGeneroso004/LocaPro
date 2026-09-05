from datetime import timedelta
from django.db.models import Sum

def verificar_disponibilidade_item(equipamento, data_inicio, data_fim, evento_ignorado=None):
    """
    Verifica se existe quantidade suficiente de um Equipamento para o período.
    Inclui 24h de buffer logístico antes e depois.
    """
    from eventos.models import Evento, ItemEvento
    
    # Buffer logístico de 24h
    bloqueio_inicio = data_inicio - timedelta(hours=24)
    bloqueio_fim = data_fim + timedelta(hours=24)

    # Busca eventos ativos que conflitam com essa data
    eventos_conflitantes = Evento.objects.filter(
        status__in=['agendado', 'em_andamento'],
        data_inicio__lte=bloqueio_fim,
        data_fim__gte=bloqueio_inicio
    )
    
    if evento_ignorado:
        eventos_conflitantes = eventos_conflitantes.exclude(pk=evento_ignorado.pk)

    # Soma quantos deste equipamento estão alugados nestes eventos
    quantidade_alugada = ItemEvento.objects.filter(
        equipamento=equipamento,
        evento__in=eventos_conflitantes
    ).aggregate(total=Sum('quantidade'))['total'] or 0
    
    return (equipamento.quantidade_total - quantidade_alugada) > 0

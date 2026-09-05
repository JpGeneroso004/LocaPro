from datetime import datetime, time, timedelta
from django.db.models import Q
from django.utils import timezone
from eventos.models import Evento

def _make_aware_safe(dt):
    if timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt

def verificar_disponibilidade_item(item, data_montagem_nova, data_desmontagem_nova, evento_id_ignorado=None):
    """
    Verifica se um item (Tenda ou ConjuntoPalco) está disponível.
    Implementa buffer logístico de 24h e regras de transição no mesmo dia.
    Retorna (True, None) ou (False, 'Mensagem de conflito').
    """
    from inventario.models import Tenda, ConjuntoPalco
    
    data_montagem_nova = _make_aware_safe(data_montagem_nova)
    data_desmontagem_nova = _make_aware_safe(data_desmontagem_nova)
    
    nome_item = getattr(item, 'codigo', getattr(item, 'nome', str(item)))
    
    if item.status == 'manutencao':
        return False, f"O item {nome_item} está em manutenção."
    if item.status == 'baixado':
        return False, f"O item {nome_item} foi descartado/vendido e não pode ser agendado."

    filtros = Q(status__in=['agendado', 'em_andamento'])
    if isinstance(item, Tenda):
        filtros &= Q(tendas=item)
    else:
        filtros &= Q(conjuntos=item)
        
    eventos_bd = Evento.objects.filter(filtros)
    if evento_id_ignorado:
        eventos_bd = eventos_bd.exclude(pk=evento_id_ignorado)
        
    for ev in eventos_bd:
        ev_dt_inicio = _make_aware_safe(datetime.combine(ev.data_inicio, ev.hora_inicio if ev.hora_inicio else time.min))
        ev_dt_fim = _make_aware_safe(datetime.combine(ev.data_fim, ev.hora_fim if ev.hora_fim else time.max))
        
        # Bloqueio inicia 24h antes da montagem agendada (buffer logístico)
        ev_dt_bloqueio_inicio = ev_dt_inicio - timedelta(hours=24)
        
        # Verifica sobreposição de tempo
        if data_montagem_nova <= ev_dt_fim and data_desmontagem_nova >= ev_dt_bloqueio_inicio:
            
            # É transição no mesmo dia? (Nova montagem ocorre no mesmo dia da desmontagem do evento antigo)
            if data_montagem_nova.date() == ev_dt_fim.date():
                if ev_dt_fim <= data_montagem_nova:
                    # Horários são válidos (desmontagem anterior <= montagem nova)
                    # Verifica se tem outro idêntico livre
                    item_livre = _buscar_item_identico_livre(item, data_montagem_nova, data_desmontagem_nova, evento_id_ignorado)
                    if item_livre:
                        nome_livre = getattr(item_livre, 'codigo', getattr(item_livre, 'nome', str(item_livre)))
                        return False, f"O item {nome_item} tem uma transição apertada neste dia pelo evento '{ev.nome}' até {ev_dt_fim.strftime('%d/%m/%Y %H:%M')}. Existe uma opção idêntica e 100% livre: selecione '{nome_livre}'."
                    else:
                        # Não há opção idêntica, mas o horário permite transição
                        return True, None
                else:
                    return False, f"O item {nome_item} está em uso pelo evento '{ev.nome}' até {ev_dt_fim.strftime('%d/%m/%Y %H:%M')}. A nova montagem precisaria ser APÓS esse horário."
            
            return False, f"O item {nome_item} está em uso/preparação pelo evento '{ev.nome}' até {ev_dt_fim.strftime('%d/%m/%Y %H:%M')}."
            
    return True, None

def _buscar_item_identico_livre(item, dt_inicio, dt_fim, evento_id_ignorado=None):
    from inventario.models import Tenda, ConjuntoPalco
    
    dt_inicio = _make_aware_safe(dt_inicio)
    dt_fim = _make_aware_safe(dt_fim)
    
    if isinstance(item, Tenda):
        similares = Tenda.objects.filter(status='ativo', tamanho=item.tamanho, tipo=item.tipo).exclude(pk=item.pk)
    else:
        similares = ConjuntoPalco.objects.filter(status='ativo').exclude(pk=item.pk)
        
    for sim in similares:
        filtros = Q(status__in=['agendado', 'em_andamento'])
        if isinstance(item, Tenda):
            filtros &= Q(tendas=sim)
        else:
            filtros &= Q(conjuntos=sim)
            
        evs = Evento.objects.filter(filtros)
        if evento_id_ignorado:
            evs = evs.exclude(pk=evento_id_ignorado)
            
        livre = True
        for ev in evs:
            e_inicio = _make_aware_safe(datetime.combine(ev.data_inicio, ev.hora_inicio if ev.hora_inicio else time.min))
            e_fim = _make_aware_safe(datetime.combine(ev.data_fim, ev.hora_fim if ev.hora_fim else time.max))
            e_bloq = e_inicio - timedelta(hours=24)
            
            if dt_inicio <= e_fim and dt_fim >= e_bloq:
                livre = False
                break
                
        if livre:
            return sim
    return None

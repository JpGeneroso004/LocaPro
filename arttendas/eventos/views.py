from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import urllib.request
import urllib.parse
from .models import Evento
from .forms import EventoForm
from inventario.models import Tenda, ConjuntoPalco

def geocode_address(rua, numero, cidade):
    try:
        # Tenta remover s/n para evitar que a API falhe na busca exata
        num = str(numero).lower().replace('s/n', '').replace('sn', '').replace('sem numero', '').strip()
        query = f"{rua} {num}, {cidade}" if num else f"{rua}, {cidade}"
        
        url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(query) + "&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'LocaPro-SaaS/1.0 (contato@locapro.com)'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode())
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                # Fallback só para a cidade
                query_fallback = cidade
                url_fb = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(query_fallback) + "&format=json&limit=1"
                req_fb = urllib.request.Request(url_fb, headers={'User-Agent': 'LocaPro-SaaS/1.0 (contato@locapro.com)'})
                with urllib.request.urlopen(req_fb, timeout=1.5) as resp_fb:
                    data_fb = json.loads(resp_fb.read().decode())
                    if data_fb:
                        return data_fb[0]['lat'], data_fb[0]['lon']
    except Exception:
        pass
    return None, None

def dashboard(request):
    hoje = timezone.localdate()
    eventos = Evento.objects.all()

    total_eventos = eventos.count()
    ativos     = eventos.filter(status__in=['agendado', 'em_andamento']).count()
    concluidos = eventos.filter(status='concluido').count()
    cancelados = eventos.filter(status='cancelado').count()

    proximos     = eventos.filter(data_inicio__gte=hoje, status='agendado').order_by('data_inicio')[:5]
    em_andamento = eventos.filter(status='em_andamento').order_by('data_fim')

    eventos_ativos_hoje = eventos.filter(
        status__in=['agendado', 'em_andamento'],
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    ).prefetch_related('tendas', 'conjuntos')
    
    tendas_ids_em_uso = set(tid for tid in eventos_ativos_hoje.values_list('tendas__id', flat=True) if tid)
    total_tendas = Tenda.objects.count()
    tendas_em_uso = len(tendas_ids_em_uso)
    tendas_manutencao = Tenda.objects.filter(status='manutencao').count()
    tendas_disponiveis = total_tendas - tendas_em_uso - tendas_manutencao

    # Considerar conjuntos globais da locadora (exceto baixados)
    todos_conjuntos = ConjuntoPalco.objects.exclude(status='baixado')
    total_placas = sum(c.quantidade_placas for c in todos_conjuntos)
    
    # Placas em uso HOJE
    placas_em_uso = sum(e.total_placas() for e in eventos_ativos_hoje)
    
    # Considerar também conjuntos em manutenção
    placas_manutencao = sum(c.quantidade_placas for c in todos_conjuntos if c.status == 'manutencao')
    
    placas_disponiveis = max(0, total_placas - placas_em_uso - placas_manutencao)

    eventos_mapa = []
    for e in eventos.filter(latitude__isnull=False, longitude__isnull=False):
        eventos_mapa.append({
            'nome': e.nome, 'cliente': e.cliente,
            'local': f"{e.rua}, {e.numero} - {e.setor}", 'cidade': e.cidade,
            'data_inicio': str(e.data_inicio), 'data_fim': str(e.data_fim),
            'status': e.get_status_display(), 'status_key': e.status,
            'tendas': e.total_tendas(), 'placas': e.total_placas(),
            'lat': float(e.latitude), 'lng': float(e.longitude),
            'url': f'/eventos/{e.pk}/',
        })

    # Calcular faturamento mensal
    from .models import Contrato
    mes_atual = hoje.month
    ano_atual = hoje.year
    contratos_mes = Contrato.objects.filter(criado_em__year=ano_atual, criado_em__month=mes_atual)
    faturamento_mes = sum(c.valor_final for c in contratos_mes)
    
    # Previsão baseada nos agendados/em andamento
    eventos_futuros = eventos.filter(status__in=['agendado', 'em_andamento'], contrato__isnull=False)
    previsao_faturamento = sum(e.contrato.valor_final for e in eventos_futuros)

    # --- BI FINANCEIRO E MÉTRICAS ---
    from django.db.models import Sum, Count
    
    # Faturamento do Mês Atual (Eventos concluídos ou agendados/em andamento neste mês)
    eventos_mes = eventos.filter(data_inicio__month=hoje.month, data_inicio__year=hoje.year, contrato__isnull=False)
    faturamento_mes = sum(e.contrato.valor_final for e in eventos_mes.exclude(status='cancelado'))
    
    # Receita Anual (Eventos deste ano)
    eventos_ano = eventos.filter(data_inicio__year=hoje.year, contrato__isnull=False).exclude(status='cancelado')
    faturamento_ano = sum(e.contrato.valor_final for e in eventos_ano)
    
    # Tenda mais popular (Mais alugada)
    tenda_mais_alugada = Tenda.objects.filter(eventos__in=eventos.exclude(status='cancelado')).annotate(num_alugueis=Count('eventos')).order_by('-num_alugueis').first()

    context = {
        'total_eventos': total_eventos, 'ativos': ativos,
        'concluidos': concluidos, 'cancelados': cancelados,
        'proximos': proximos, 'em_andamento': em_andamento,
        'total_tendas': total_tendas,
        'tendas_disponiveis': tendas_disponiveis, 'tendas_em_uso': tendas_em_uso,
        'total_placas': total_placas,
        'placas_em_uso': placas_em_uso, 'placas_disponiveis': placas_disponiveis,
        'eventos_mapa_json': json.dumps(eventos_mapa, ensure_ascii=False),
        'faturamento_mes': faturamento_mes,
        'previsao_faturamento': previsao_faturamento,
        'faturamento_ano': faturamento_ano,
        'tenda_mais_alugada': tenda_mais_alugada,
    }
    return render(request, 'eventos/dashboard.html', context)


from django.core.paginator import Paginator

def lista_eventos(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    eventos_list = Evento.objects.all()
    if q:
        eventos_list = eventos_list.filter(
            Q(nome__icontains=q) | Q(cliente__icontains=q) |
            Q(rua__icontains=q) | Q(setor__icontains=q) | Q(cidade__icontains=q))
    if status:
        eventos_list = eventos_list.filter(status=status)
        
    paginator = Paginator(eventos_list, 20)
    page_number = request.GET.get('page')
    eventos = paginator.get_page(page_number)
    
    return render(request, 'eventos/lista.html', {'eventos': eventos, 'q': q, 'status': status})


def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalhe.html', {'evento': evento})


def novo_evento(request):
    initial_data = {}
    reutilizar = request.GET.get('reutilizar')
    if reutilizar:
        old = Evento.objects.filter(pk=reutilizar).first()
        if old:
            initial_data = {
                'cliente': old.cliente, 'telefone': old.telefone,
                'rua': old.rua, 'numero': old.numero, 'setor': old.setor,
                'complemento': old.complemento, 'cidade': old.cidade,
                'tendas': old.tendas.all(),
                'conjuntos': old.conjuntos.all()
            }
            messages.info(request, f'Preenchido com os dados e materiais do evento "{old.nome}". Defina a nova data.')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if hasattr(request.user, 'organizacao'):
                evento.organizacao = request.user.organizacao
                
            # Smart LocaPoints Cliente Generation
            if evento.cliente:
                from .models import Cliente
                cli = Cliente.objects.filter(nome__iexact=evento.cliente, organizacao=evento.organizacao).first()
                if not cli:
                    cli = Cliente.objects.create(nome=evento.cliente, telefone=evento.telefone, organizacao=evento.organizacao)
                evento.cliente_fidelidade = cli
            
            from inventario.utils import verificar_disponibilidade_item
            from datetime import datetime, time
            data_montagem_nova = datetime.combine(evento.data_inicio, evento.hora_inicio if evento.hora_inicio else time.min)
            data_desmontagem_nova = datetime.combine(evento.data_fim, evento.hora_fim if evento.hora_fim else time.max)
            
            if data_desmontagem_nova <= data_montagem_nova:
                messages.error(request, "A desmontagem deve ser posterior à montagem.")
                return render(request, 'eventos/form_evento.html', {
                    'form': form, 'titulo': 'Novo Evento', 'is_reutilizar': bool(reutilizar)
                })

            if data_montagem_nova.date() < timezone.localdate():
                messages.error(request, "A data de montagem não pode ser no passado.")
                return render(request, 'eventos/form_evento.html', {
                    'form': form, 'titulo': 'Novo Evento', 'is_reutilizar': bool(reutilizar)
                })

            
            conflitos = []
            for t in form.cleaned_data.get('tendas', []):
                valido, msg = verificar_disponibilidade_item(t, data_montagem_nova, data_desmontagem_nova)
                if not valido: conflitos.append(msg)
                
            for c in form.cleaned_data.get('conjuntos', []):
                valido, msg = verificar_disponibilidade_item(c, data_montagem_nova, data_desmontagem_nova)
                if not valido: conflitos.append(msg)
                
            if conflitos:
                for c in conflitos:
                    messages.error(request, c)
            else:
                lat, lng = geocode_address(evento.rua, evento.numero, evento.cidade)
                evento.latitude = lat
                evento.longitude = lng
                evento.save()
                form.save_m2m()
                messages.success(request, f'Evento "{evento.nome}" criado com sucesso!')
                return redirect('eventos:detalhe', pk=evento.pk)
    else:
        form = EventoForm(initial=initial_data)
    return render(request, 'eventos/form_evento.html', {
        'form': form, 'titulo': 'Novo Evento', 'is_reutilizar': bool(reutilizar)
    })


def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            ev = form.save(commit=False)
            
            # Smart LocaPoints Cliente Generation
            if ev.cliente:
                from .models import Cliente
                cli = Cliente.objects.filter(nome__iexact=ev.cliente, organizacao=ev.organizacao).first()
                if not cli:
                    cli = Cliente.objects.create(nome=ev.cliente, telefone=ev.telefone, organizacao=ev.organizacao)
                ev.cliente_fidelidade = cli
            
            from inventario.utils import verificar_disponibilidade_item
            from datetime import datetime, time
            data_montagem_nova = datetime.combine(ev.data_inicio, ev.hora_inicio if ev.hora_inicio else time.min)
            data_desmontagem_nova = datetime.combine(ev.data_fim, ev.hora_fim if ev.hora_fim else time.max)
            
            conflitos = []
            if ev.status in ['agendado', 'em_andamento']:
                for t in form.cleaned_data.get('tendas', []):
                    valido, msg = verificar_disponibilidade_item(t, data_montagem_nova, data_desmontagem_nova, evento_id_ignorado=ev.pk)
                    if not valido: conflitos.append(msg)
                    
                for c in form.cleaned_data.get('conjuntos', []):
                    valido, msg = verificar_disponibilidade_item(c, data_montagem_nova, data_desmontagem_nova, evento_id_ignorado=ev.pk)
                    if not valido: conflitos.append(msg)
            
            if conflitos:
                for c in conflitos:
                    messages.error(request, c)
            else:
                if 'rua' in form.changed_data or 'numero' in form.changed_data or 'cidade' in form.changed_data:
                    lat, lng = geocode_address(ev.rua, ev.numero, ev.cidade)
                    ev.latitude = lat
                    ev.longitude = lng
                ev.save()
                form.save_m2m()
                messages.success(request, 'Evento atualizado com sucesso!')
                return redirect('eventos:detalhe', pk=ev.pk)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/form_evento.html', {
        'form': form, 'titulo': 'Editar Evento', 'evento': evento
    })


def excluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        nome = evento.nome
        evento.delete()
        messages.success(request, f'Evento "{nome}" removido com sucesso!')
        return redirect('eventos:lista')
    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})

@login_required
def concluir_evento(request, pk):
    # Quando o evento é concluído, gera os LocaPoints para o cliente
    evento = get_object_or_404(Evento, pk=pk)
    org = request.user.organizacao
    
    if evento.status != 'concluido':
        evento.status = 'concluido'
        evento.save()
        
        # Gera LocaPoints se tiver contrato e fidelidade ativa
        if hasattr(evento, 'contrato') and org and org.fidelidade_ativa:
            contrato = evento.contrato
            if not contrato.pontos_creditados and evento.cliente_fidelidade:
                pontos = int(contrato.valor_final * org.pontos_por_real)
                
                # Soma na carteira do cliente
                cliente = evento.cliente_fidelidade
                cliente.locapoints += pontos
                cliente.save()
                
                # Registra no contrato
                contrato.pontos_gerados = pontos
                contrato.pontos_creditados = True
                contrato.save()
                
                messages.success(request, f'Evento concluído! {pontos} LocaPoints foram adicionados à carteira de {cliente.nome}.')
            else:
                messages.success(request, 'Evento marcado como concluído!')
        else:
            messages.success(request, 'Evento marcado como concluído!')
            
    return redirect('eventos:detalhe', pk=evento.pk)

@login_required
def aplicar_desconto_fidelidade(request, pk):
    # Aplica o desconto usando os pontos do cliente no contrato atual
    contrato = get_object_or_404(Contrato, pk=pk)
    evento = contrato.evento
    org = request.user.organizacao
    
    if request.method == 'POST' and org and org.fidelidade_ativa and evento.cliente_fidelidade:
        cliente = evento.cliente_fidelidade
        
        if cliente.locapoints > 0:
            # Calcula o valor do desconto
            desconto = cliente.locapoints / org.taxa_resgate
            
            # Limita o desconto ao valor do contrato
            if desconto > contrato.valor_total:
                desconto = contrato.valor_total
                pontos_gastos = int(desconto * org.taxa_resgate)
            else:
                pontos_gastos = cliente.locapoints
                
            # Desconta da carteira
            cliente.locapoints -= pontos_gastos
            cliente.save()
            
            # Aplica no contrato
            contrato.pontos_utilizados += pontos_gastos
            contrato.desconto_fidelidade += desconto
            contrato.save()
            
            messages.success(request, f'Sucesso! {pontos_gastos} pontos foram resgatados, gerando R$ {desconto:.2f} de desconto.')
        else:
            messages.warning(request, 'Este cliente não possui pontos suficientes.')
            
    return redirect('eventos:detalhe', pk=evento.pk)

def contratos_lista(request):
    from .models import Contrato, Evento
    contratos_list = Contrato.objects.all().order_by('-criado_em')
    
    paginator = Paginator(contratos_list, 20)
    page_number = request.GET.get('page')
    contratos = paginator.get_page(page_number)
    
    eventos_sem_contrato = Evento.objects.filter(contrato__isnull=True).exclude(status='cancelado').order_by('-data_inicio')[:20]
    return render(request, 'eventos/contratos_lista.html', {
        'contratos': contratos, 
        'eventos_sem_contrato': eventos_sem_contrato
    })

def gerar_contrato(request, evento_id):
    from .models import Contrato
    evento = get_object_or_404(Evento, pk=evento_id)
    if hasattr(evento, 'contrato'):
        return redirect('eventos:imprimir_contrato', contrato_id=evento.contrato.id)

    contratante_nome = evento.cliente
    contratante_telefone = evento.telefone
    endereco_montagem = f"{evento.rua}, {evento.numero} - {evento.setor}"
    if evento.complemento:
        endereco_montagem += f" - {evento.complemento}"
    endereco_montagem += f" - {evento.cidade}"
    
    itens = []
    if evento.tendas.exists():
        for t in evento.tendas.all():
            itens.append(f"Tenda {t.tamanho} ({t.tipo})")
    if evento.conjuntos.exists():
        for c in evento.conjuntos.all():
            itens.append(f"Conjunto {c.nome} ({c.quantidade_placas} placas de 1x1m)")
    itens_locados = "\n".join(itens) if itens else "Nenhum item especificado."
    
    clausulas_padrao = ""
    if hasattr(request.user, 'organizacao') and request.user.organizacao:
        clausulas_padrao = request.user.organizacao.clausulas_padrao

    data_montagem_padrao = ''
    data_desmontagem_padrao = ''
    if evento.data_inicio:
        hora_i = evento.hora_inicio.strftime('%H:%M') if evento.hora_inicio else '08:00'
        data_montagem_padrao = f"{evento.data_inicio.strftime('%Y-%m-%d')}T{hora_i}"
    
    if evento.data_fim:
        hora_f = evento.hora_fim.strftime('%H:%M') if evento.hora_fim else '18:00'
        data_desmontagem_padrao = f"{evento.data_fim.strftime('%Y-%m-%d')}T{hora_f}"

    context = {
        'evento': evento,
        'contratante_nome': contratante_nome,
        'contratante_telefone': contratante_telefone,
        'endereco_montagem': endereco_montagem,
        'itens_locados': itens_locados,
        'clausulas_padrao': clausulas_padrao,
        'data_montagem_padrao': data_montagem_padrao,
        'data_desmontagem_padrao': data_desmontagem_padrao,
    }
    return render(request, 'eventos/form_contrato.html', context)

def limpar_moeda(val):
    if not val:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_limpo = str(val).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(val_limpo)
    except ValueError:
        return 0.0

def salvar_contrato(request, evento_id):
    import traceback
    from datetime import datetime
    from .models import Contrato
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        try:
            contrato, created = Contrato.objects.get_or_create(evento=evento)
            if created or not contrato.organizacao:
                contrato.organizacao = evento.organizacao
            contrato.contratante_nome = request.POST.get('contratante_nome', '')
            contrato.contratante_cpf_cnpj = request.POST.get('contratante_cpf_cnpj', '')
            contrato.contratante_telefone = request.POST.get('contratante_telefone', '')
            contrato.contratante_endereco = request.POST.get('contratante_endereco', '')
            
            # Parsing Seguro de Datas
            dm = request.POST.get('data_montagem', '').strip()
            if dm:
                try:
                    contrato.data_montagem = datetime.fromisoformat(dm)
                except ValueError:
                    contrato.data_montagem = None
            else:
                contrato.data_montagem = None
                
            dd = request.POST.get('data_desmontagem', '').strip()
            if dd:
                try:
                    contrato.data_desmontagem = datetime.fromisoformat(dd)
                except ValueError:
                    contrato.data_desmontagem = None
            else:
                contrato.data_desmontagem = None
            
            contrato.endereco_montagem = request.POST.get('endereco_montagem', '')
            
            # Tratamento de Valores Monetários
            contrato.valor_total = limpar_moeda(request.POST.get('valor_total'))
            contrato.sinal = limpar_moeda(request.POST.get('sinal'))
                
            contrato.forma_pagamento = request.POST.get('forma_pagamento', '')
            contrato.itens_locados = request.POST.get('itens_locados', '')
            contrato.clausulas = request.POST.get('clausulas', '')
            
            contrato.save()
            
            messages.success(request, 'Contrato salvo com sucesso!')
            return redirect('eventos:imprimir_contrato', contrato_id=contrato.id)
            
        except Exception as e:
            traceback.print_exc()
            messages.error(request, f'Erro inesperado ao salvar contrato: {str(e)}')
            return redirect('eventos:detalhe', pk=evento.pk)

    return redirect('eventos:contratos_lista')


def imprimir_contrato(request, contrato_id):
    from .models import Contrato
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    return render(request, 'eventos/imprimir_contrato.html', {'contrato': contrato})

def deletar_contrato(request, contrato_id):
    from .models import Contrato
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    if request.method == 'POST':
        contrato.delete()
        messages.success(request, 'Contrato removido.')
        return redirect('eventos:contratos_lista')
    return redirect('eventos:contratos_lista')


from django.http import JsonResponse
from inventario.models import Tenda, ConjuntoPalco
from inventario.utils import verificar_disponibilidade_item
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def obter_equipamentos_disponiveis(request):
    try:
        inicio_str = request.GET.get('inicio')
        fim_str = request.GET.get('fim')
        evento_id = request.GET.get('evento_id')
        
        if evento_id and str(evento_id).isdigit():
            evento_id = int(evento_id)
        else:
            evento_id = None
            
        if not inicio_str or not fim_str:
            return JsonResponse({'sucesso': True, 'tendas': [], 'conjuntos': []})
            
        def parse_date(date_str):
            try:
                return datetime.fromisoformat(date_str.replace('T', ' '))
            except ValueError:
                pass
                
            try:
                return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
            except ValueError:
                pass
                
            try:
                return datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                pass
                
            raise ValueError(f"Formato de data inválido: {date_str}")
            
        try:
            inicio_dt = parse_date(inicio_str)
            fim_dt = parse_date(fim_str)
            
            if fim_dt <= inicio_dt:
                return JsonResponse({'sucesso': False, 'erro': 'Intervalo de datas inválido'}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)
            
        from django.utils import timezone
        if timezone.is_naive(inicio_dt):
            inicio_dt = timezone.make_aware(inicio_dt)
        if timezone.is_naive(fim_dt):
            fim_dt = timezone.make_aware(fim_dt)
            
        from datetime import timedelta, time
        
        from .models import Evento
        eventos_ativos = Evento.objects.filter(status__in=['agendado', 'em_andamento'])
        if evento_id:
            eventos_ativos = eventos_ativos.exclude(id=evento_id)
            
        tendas_ocupadas_ids = set()
        conjuntos_ocupados_ids = set()
        
        for ev in eventos_ativos:
            ev_dt_inicio = datetime.combine(ev.data_inicio, ev.hora_inicio if ev.hora_inicio else time.min)
            ev_dt_fim = datetime.combine(ev.data_fim, ev.hora_fim if ev.hora_fim else time.max)
            
            if timezone.is_naive(ev_dt_inicio):
                ev_dt_inicio = timezone.make_aware(ev_dt_inicio)
            if timezone.is_naive(ev_dt_fim):
                ev_dt_fim = timezone.make_aware(ev_dt_fim)
                
            ev_dt_bloqueio_inicio = ev_dt_inicio - timedelta(hours=24)
                
            if inicio_dt <= ev_dt_fim and fim_dt >= ev_dt_bloqueio_inicio:
                tendas_ocupadas_ids.update(ev.tendas.values_list('id', flat=True))
                conjuntos_ocupados_ids.update(ev.conjuntos.values_list('id', flat=True))
                
        tendas_livres = Tenda.objects.filter(status='ativo').exclude(id__in=tendas_ocupadas_ids)
        conjuntos_livres = ConjuntoPalco.objects.filter(status='ativo').exclude(id__in=conjuntos_ocupados_ids)
        
        return JsonResponse({
            'sucesso': True,
            'tendas': [{'id': t.id, 'nome': str(t)} for t in tendas_livres],
            'conjuntos': [{'id': c.id, 'nome': str(c)} for c in conjuntos_livres]
        })
        
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

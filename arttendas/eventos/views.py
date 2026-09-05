from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Evento, Cliente, Contrato, ItemEvento
from inventario.models import Equipamento
from .forms import EventoForm
from django.http import JsonResponse
import traceback
from django.db.models import Sum

@login_required
def painel_eventos(request):
    eventos = Evento.objects.all()
    hoje = timezone.localdate()
    eventos_ativos_hoje = eventos.filter(status__in=['agendado', 'em_andamento'], data_inicio__lte=hoje, data_fim__gte=hoje)
    
    total_equipamentos = sum(e.quantidade_total for e in Equipamento.objects.filter(status='ativo'))
    equip_em_uso = sum(ie.quantidade for ev in eventos_ativos_hoje for ie in ev.itens.all())
    equip_disponivel = total_equipamentos - equip_em_uso
    
    eventos_info = []
    for e in eventos_ativos_hoje:
        eventos_info.append({
            'evento': e,
            'itens': e.total_itens()
        })
        
    context = {
        'eventos': eventos,
        'eventos_ativos_hoje': eventos_info,
        'total_equipamentos': total_equipamentos,
        'equip_disponivel': equip_disponivel,
        'equip_em_uso': equip_em_uso,
    }
    return render(request, 'eventos/dashboard.html', context)

@login_required
def novo_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizacao = request.user.organizacao
            evento.save()
            
            # Salvar itens dinâmicos
            itens_str = request.POST.get('itens_json', '[]')
            import json
            try:
                itens = json.loads(itens_str)
                for item in itens:
                    eq_id = item.get('id')
                    qtd = int(item.get('qtd', 1))
                    eq = Equipamento.objects.get(id=eq_id, organizacao=request.user.organizacao)
                    ItemEvento.objects.create(
                        evento=evento,
                        equipamento=eq,
                        quantidade=qtd,
                        preco_fechado=eq.valor_diaria * qtd
                    )
            except Exception as e:
                print('Erro ao salvar itens:', e)
            
            messages.success(request, 'Evento cadastrado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {'form': form, 'titulo': 'Novo Evento'})

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            
            # Atualizar itens dinâmicos
            itens_str = request.POST.get('itens_json', '[]')
            import json
            try:
                itens = json.loads(itens_str)
                # Remove itens antigos para simplificar atualização
                evento.itens.all().delete()
                for item in itens:
                    eq_id = item.get('id')
                    qtd = int(item.get('qtd', 1))
                    eq = Equipamento.objects.get(id=eq_id, organizacao=request.user.organizacao)
                    ItemEvento.objects.create(
                        evento=evento,
                        equipamento=eq,
                        quantidade=qtd,
                        preco_fechado=eq.valor_diaria * qtd
                    )
            except Exception as e:
                print('Erro ao salvar itens:', e)
                
            messages.success(request, 'Evento atualizado!')
            return redirect('eventos:detalhe', pk=evento.pk)
    else:
        form = EventoForm(instance=evento)
        
    # Passa os itens atuais para o template (para preencher o JS)
    itens_atuais = [{'id': i.equipamento.id, 'nome': i.equipamento.nome, 'qtd': i.quantidade, 'max_qtd': i.equipamento.quantidade_total} for i in evento.itens.all()]
    import json
    itens_json = json.dumps(itens_atuais)
    
    return render(request, 'eventos/form_evento.html', {'form': form, 'titulo': f'Editar {evento.nome}', 'itens_atuais_json': itens_json})

@login_required
def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalhe_evento.html', {'evento': evento})

@login_required
def contratos_lista(request):
    contratos = Contrato.objects.all().order_by('-criado_em')
    return render(request, 'eventos/contratos_lista.html', {'contratos': contratos})

@login_required
def gerar_contrato(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    contrato, created = Contrato.objects.get_or_create(evento=evento)
    if created or not contrato.itens_locados:
        contrato.organizacao = evento.organizacao
        contrato.contratante_nome = evento.cliente
        contrato.endereco_montagem = f"{evento.rua}, {evento.numero} - {evento.setor}, {evento.cidade}"
        
        linhas_itens = []
        total = 0
        for item in evento.itens.all():
            linhas_itens.append(f"{item.quantidade}x {item.equipamento.nome}")
            total += item.preco_fechado
        
        contrato.itens_locados = "\n".join(linhas_itens)
        contrato.valor_total = total
        
        import uuid
        contrato.token_assinatura = str(uuid.uuid4())
        contrato.save()
        
    return render(request, 'eventos/form_contrato.html', {'contrato': contrato})

@login_required
def salvar_contrato(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        try:
            contrato, created = Contrato.objects.get_or_create(evento=evento)
            if created or not contrato.organizacao:
                contrato.organizacao = evento.organizacao
            if not contrato.token_assinatura:
                import uuid
                contrato.token_assinatura = str(uuid.uuid4())
            
            contrato.contratante_nome = request.POST.get('contratante_nome', '')
            contrato.contratante_cpf_cnpj = request.POST.get('contratante_cpf_cnpj', '')
            contrato.save()
            
            messages.success(request, 'Contrato salvo!')
            return redirect('eventos:imprimir_contrato', contrato_id=contrato.id)
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            
    return redirect('eventos:detalhe', pk=evento.pk)

def imprimir_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    return render(request, 'eventos/imprimir_contrato.html', {'contrato': contrato})

def deletar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    if request.method == 'POST':
        contrato.delete()
    return redirect('eventos:contratos_lista')

@login_required
def obter_equipamentos_disponiveis(request):
    try:
        inicio_str = request.GET.get('inicio')
        fim_str = request.GET.get('fim')
        evento_id = request.GET.get('evento_id')
        
        if not inicio_str or not fim_str:
            return JsonResponse({'sucesso': False, 'erro': 'Datas não fornecidas'}, status=400)
            
        def parse_date(date_str):
            if 'T' in date_str:
                return datetime.fromisoformat(date_str)
            return datetime.strptime(date_str, '%Y-%m-%d')
            
        try:
            dt_inicio = parse_date(inicio_str)
            dt_fim = parse_date(fim_str)
        except ValueError:
            return JsonResponse({'sucesso': False, 'erro': 'Formato de data inválido'}, status=400)
            
        if timezone.is_naive(dt_inicio): dt_inicio = timezone.make_aware(dt_inicio)
        if timezone.is_naive(dt_fim): dt_fim = timezone.make_aware(dt_fim)
            
        # Bloqueio logístico de 24h
        bloqueio_inicio = dt_inicio - timedelta(hours=24)
        bloqueio_fim = dt_fim + timedelta(hours=24)
        
        eventos_conflitantes = Evento.objects.filter(
            status__in=['agendado', 'em_andamento'],
            data_inicio__lte=bloqueio_fim,
            data_fim__gte=bloqueio_inicio,
            organizacao=request.user.organizacao
        )
        if evento_id and evento_id.isdigit():
            eventos_conflitantes = eventos_conflitantes.exclude(pk=int(evento_id))
            
        # Puxa o total alugado por equipamento nestes eventos
        from django.db.models import Sum
        alugados = ItemEvento.objects.filter(evento__in=eventos_conflitantes).values('equipamento_id').annotate(total=Sum('quantidade'))
        map_alugados = {item['equipamento_id']: item['total'] for item in alugados}
        
        equipamentos = Equipamento.objects.filter(status='ativo', organizacao=request.user.organizacao)
        res = []
        for eq in equipamentos:
            qtd_em_uso = map_alugados.get(eq.id, 0)
            qtd_livre = eq.quantidade_total - qtd_em_uso
            if qtd_livre > 0:
                res.append({
                    'id': eq.id,
                    'nome': eq.nome,
                    'qtd_livre': qtd_livre,
                    'valor': float(eq.valor_diaria)
                })
        
        return JsonResponse({'sucesso': True, 'equipamentos': res})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def assinatura_cliente(request, token):
    contrato = get_object_or_404(Contrato, token_assinatura=token)
    if request.method == 'POST':
        if contrato.status_assinatura == 'pendente':
            contrato.status_assinatura = 'assinado'
            contrato.data_assinatura = timezone.now()
            contrato.ip_assinatura = get_client_ip(request)
            contrato.save()
    return render(request, 'eventos/assinatura_cliente.html', {'contrato': contrato})

@login_required
def gerar_contrato(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    contrato, created = Contrato.objects.get_or_create(evento=evento)
    if created or not contrato.itens_locados:
        contrato.organizacao = evento.organizacao
        contrato.contratante_nome = evento.cliente
        contrato.endereco_montagem = f"{evento.rua}, {evento.numero} - {evento.setor}, {evento.cidade}"
        
        linhas_itens = []
        total = 0
        for item in evento.itens.all():
            linhas_itens.append(f"{item.quantidade}x {item.equipamento.nome}")
            total += item.preco_fechado
        
        contrato.itens_locados = '\n'.join(linhas_itens)
        contrato.valor_total = total
        
        import uuid
        contrato.token_assinatura = str(uuid.uuid4())
        contrato.save()
        
    return redirect('eventos:imprimir_contrato', contrato_id=contrato.id)

@login_required
def excluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST' or request.method == 'GET':
        evento.status = 'cancelado'
        evento.save()
        messages.success(request, 'Evento cancelado.')
    return redirect('eventos:dashboard')

@login_required
def concluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento.status = 'concluido'
    evento.save()
    messages.success(request, 'Evento concluído.')
    return redirect('eventos:dashboard')

@login_required
def aplicar_desconto_fidelidade(request, pk):
    return redirect('eventos:dashboard')

@login_required
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-data_inicio')
    return render(request, 'eventos/lista.html', {'eventos': eventos})

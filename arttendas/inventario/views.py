from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tenda, ConjuntoPalco
from .forms import TendaForm, ConjuntoPalcoForm


from datetime import date

def inventario(request):
    from eventos.models import Evento
    hoje = date.today()
    eventos_hoje = Evento.objects.filter(
        status__in=['agendado', 'em_andamento'],
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    )
    
    tendas_ids_em_uso = set(tid for tid in eventos_hoje.values_list('tendas__id', flat=True) if tid)
    conjuntos_ids_em_uso = set(cid for cid in eventos_hoje.values_list('conjuntos__id', flat=True) if cid)

    tendas = list(Tenda.objects.all().order_by('tamanho', 'tipo', 'codigo'))
    
    total_tendas = len(tendas)
    tendas_em_uso = 0
    tendas_manutencao = 0
    tendas_disponiveis = 0
    total_piramisais = 0
    total_chapeu = 0
    piramisais_disponiveis = 0
    chapeu_disponiveis = 0

    for t in tendas:
        if t.tipo == 'piramidal':
            total_piramisais += 1
        else:
            total_chapeu += 1
            
        if t.status == 'manutencao':
            t.current_state = 'manutencao'
            tendas_manutencao += 1
        elif t.id in tendas_ids_em_uso:
            t.current_state = 'em_uso'
            tendas_em_uso += 1
        else:
            t.current_state = 'disponivel'
            tendas_disponiveis += 1
            if t.tipo == 'piramidal':
                piramisais_disponiveis += 1
            else:
                chapeu_disponiveis += 1

    # Conjuntos de palco/piso
    conjuntos = list(ConjuntoPalco.objects.all())
    total_placas = sum(c.quantidade_placas for c in conjuntos)
    placas_em_uso = 0
    placas_manutencao = 0
    
    conjuntos_em_uso = 0
    conjuntos_manutencao = 0
    conjuntos_disponiveis = 0

    for c in conjuntos:
        if c.status == 'manutencao':
            c.current_state = 'manutencao'
            placas_manutencao += c.quantidade_placas
            conjuntos_manutencao += 1
        elif c.id in conjuntos_ids_em_uso:
            c.current_state = 'em_uso'
            placas_em_uso += c.quantidade_placas
            conjuntos_em_uso += 1
        else:
            c.current_state = 'disponivel'
            conjuntos_disponiveis += 1
            
    placas_disponiveis = total_placas - placas_em_uso - placas_manutencao

    # Painel visual por tamanho
    ORDEM = ['10x10', '8x8', '7x7', '6x6', '5x5', '4x4', '3x3']
    estoque_resumo = []
    for tam in ORDEM:
        piramisais = [t for t in tendas if t.tamanho == tam and t.tipo == 'piramidal']
        chapeu     = [t for t in tendas if t.tamanho == tam and t.tipo == 'chapeu_bruxa']
        if piramisais or chapeu:
            estoque_resumo.append({
                'tamanho': f'Tenda {tam} m',
                'piramisais': piramisais,
                'chapeu': chapeu,
            })

    context = {
        'tendas': tendas,
        'total_tendas': total_tendas,
        'tendas_disponiveis': tendas_disponiveis,
        'tendas_em_uso': tendas_em_uso,
        'tendas_manutencao': tendas_manutencao,
        'total_piramisais': total_piramisais,
        'total_chapeu': total_chapeu,
        'piramisais_disponiveis': piramisais_disponiveis,
        'chapeu_disponiveis': chapeu_disponiveis,
        'estoque_resumo': estoque_resumo,
        'conjuntos': conjuntos,
        'total_placas': total_placas,
        'placas_em_uso': placas_em_uso,
        'placas_disponiveis': placas_disponiveis,
        'placas_manutencao': placas_manutencao,
        'conjuntos_disponiveis': conjuntos_disponiveis,
        'conjuntos_em_uso': conjuntos_em_uso,
        'conjuntos_manutencao': conjuntos_manutencao,
    }
    return render(request, 'inventario/inventario.html', context)


# ── Tendas ────────────────────────────────────────────────
def nova_tenda(request):
    if request.method == 'POST':
        form = TendaForm(request.POST)
        if form.is_valid():
            tenda = form.save(commit=False)
            if hasattr(request.user, 'organizacao'):
                tenda.organizacao = request.user.organizacao
            tenda.save()
            messages.success(request, 'Tenda cadastrada com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = TendaForm()
    return render(request, 'inventario/form_tenda.html', {'form': form, 'titulo': 'Nova Tenda'})


def editar_tenda(request, pk):
    tenda = get_object_or_404(Tenda, pk=pk)
    if request.method == 'POST':
        form = TendaForm(request.POST, instance=tenda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenda atualizada com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = TendaForm(instance=tenda)
    return render(request, 'inventario/form_tenda.html', {
        'form': form, 'titulo': f'Editar {tenda.codigo}', 'tenda': tenda
    })


def excluir_tenda(request, pk):
    tenda = get_object_or_404(Tenda, pk=pk)
    if request.method == 'POST':
        # BLINDAGEM: Impedir deleção se a tenda estiver atrelada a eventos ativos/futuros
        em_uso = tenda.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: A Tenda {tenda.codigo} não pode ser excluída pois está reservada ou em uso em um evento ativo.')
        else:
            cod = tenda.codigo
            tenda.delete()
            messages.success(request, f'Tenda {cod} removida com sucesso!')
    return redirect('inventario:inventario')


# ── Conjuntos de Palco/Piso ───────────────────────────────
def novo_conjunto(request):
    if request.method == 'POST':
        form = ConjuntoPalcoForm(request.POST)
        if form.is_valid():
            conjunto = form.save(commit=False)
            if hasattr(request.user, 'organizacao'):
                conjunto.organizacao = request.user.organizacao
            conjunto.save()
            messages.success(request, 'Conjunto cadastrado com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = ConjuntoPalcoForm()
    return render(request, 'inventario/form_conjunto.html', {'form': form, 'titulo': 'Novo Conjunto de Palco/Piso'})


def editar_conjunto(request, pk):
    conjunto = get_object_or_404(ConjuntoPalco, pk=pk)
    if request.method == 'POST':
        form = ConjuntoPalcoForm(request.POST, instance=conjunto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conjunto atualizado com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = ConjuntoPalcoForm(instance=conjunto)
    return render(request, 'inventario/form_conjunto.html', {
        'form': form, 'titulo': f'Editar {conjunto.nome}', 'conjunto': conjunto
    })


def excluir_conjunto(request, pk):
    conjunto = get_object_or_404(ConjuntoPalco, pk=pk)
    if request.method == 'POST':
        em_uso = conjunto.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: O Conjunto "{conjunto.nome}" não pode ser excluído pois está reservado ou em uso em um evento ativo.')
        else:
            nome = conjunto.nome
            conjunto.delete()
            messages.success(request, f'Conjunto "{nome}" removido com sucesso!')
    return redirect('inventario:inventario')

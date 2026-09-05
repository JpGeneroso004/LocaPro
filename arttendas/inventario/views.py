from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Equipamento, CategoriaEquipamento
from .forms import EquipamentoForm
from eventos.models import Evento, ItemEvento

@login_required
def painel_estoque(request):
    equipamentos = Equipamento.objects.filter(status='ativo').order_by('categoria__nome', 'nome')
    inativos = Equipamento.objects.filter(status='inativo')
    
    total_equipamentos = sum(e.quantidade_total for e in equipamentos)
    
    hoje = timezone.localdate()
    eventos_hoje = Evento.objects.filter(
        status__in=['agendado', 'em_andamento'],
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    )
    
    # Itens em uso hoje
    itens_em_uso = ItemEvento.objects.filter(evento__in=eventos_hoje)
    total_em_uso = sum(item.quantidade for item in itens_em_uso)
    
    context = {
        'equipamentos': equipamentos,
        'inativos': inativos,
        'total_equipamentos': total_equipamentos,
        'equipamentos_em_uso': total_em_uso,
        'equipamentos_disponiveis': total_equipamentos - total_em_uso
    }
    return render(request, 'inventario/painel.html', context)


@login_required
def novo_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        form.fields['categoria'].queryset = CategoriaEquipamento.objects.filter(organizacao=request.user.organizacao)
        if form.is_valid():
            eq = form.save(commit=False)
            eq.organizacao = request.user.organizacao
            eq.save()
            messages.success(request, 'Item cadastrado com sucesso!')
            return redirect('inventario:painel')
    else:
        form = EquipamentoForm()
        form.fields['categoria'].queryset = CategoriaEquipamento.objects.filter(organizacao=request.user.organizacao)
        
    return render(request, 'inventario/form_equipamento.html', {'form': form, 'titulo': 'Novo Equipamento'})

@login_required
def editar_equipamento(request, pk):
    eq = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=eq)
        form.fields['categoria'].queryset = CategoriaEquipamento.objects.filter(organizacao=request.user.organizacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado!')
            return redirect('inventario:painel')
    else:
        form = EquipamentoForm(instance=eq)
        form.fields['categoria'].queryset = CategoriaEquipamento.objects.filter(organizacao=request.user.organizacao)
        
    return render(request, 'inventario/form_equipamento.html', {'form': form, 'titulo': f'Editar {eq.nome}'})

@login_required
def excluir_equipamento(request, pk):
    eq = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        if eq.alocacoes.filter(evento__status__in=['agendado', 'em_andamento']).exists():
            messages.error(request, 'Não é possível excluir um item que está alugado em um evento ativo.')
        else:
            if eq.alocacoes.exists():
                eq.status = 'inativo'
                eq.save()
                messages.warning(request, 'Este item possui histórico passado, então foi inativado ao invés de apagado.')
            else:
                eq.delete()
                messages.success(request, 'Item excluído permanentemente.')
    return redirect('inventario:painel')

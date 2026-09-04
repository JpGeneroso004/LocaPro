from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Organizacao, Usuario
from django.db import transaction

def cadastro_locadora(request):
    if request.user.is_authenticated:
        return redirect('eventos:dashboard')

    if request.method == 'POST':
        empresa_nome = request.POST.get('empresa_nome')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not (empresa_nome and nome and email and senha):
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'empresas/cadastro.html')
            
        if Usuario.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return render(request, 'empresas/cadastro.html')

        try:
            with transaction.atomic():
                org = Organizacao.objects.create(nome=empresa_nome)
                user = Usuario.objects.create_user(
                    username=email,
                    email=email,
                    password=senha,
                    first_name=nome,
                    organizacao=org
                )
            login(request, user)
            messages.success(request, f'Bem-vindo(a) ao LocaPro, {nome}! Sua conta da empresa {empresa_nome} foi criada.')
            return redirect('eventos:dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')

    return render(request, 'empresas/cadastro.html')

from django.contrib.auth.decorators import login_required
from .forms import OrganizacaoForm

@login_required
def configuracoes_empresa(request):
    org = request.user.organizacao
    if request.method == 'POST':
        form = OrganizacaoForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações da empresa atualizadas!')
            return redirect('empresas:configuracoes')
    else:
        form = OrganizacaoForm(instance=org)
    return render(request, 'empresas/configuracoes.html', {'form': form})

from django.db.models import Count
from django.core.exceptions import PermissionDenied

@login_required
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        raise PermissionDenied("Acesso restrito ao dono do SaaS.")
    
    orgs = Organizacao.objects.annotate(
        total_usuarios=Count('usuarios', distinct=True),
        total_eventos=Count('eventos', distinct=True),
        total_tendas=Count('tendas', distinct=True)
    ).order_by('-criado_em')
    
    context = {
        'orgs': orgs,
        'total_clientes': orgs.count(),
        'total_eventos_global': sum(o.total_eventos for o in orgs)
    }
    return render(request, 'empresas/super_admin.html', context)

@login_required
def lista_equipe(request):
    usuarios = Usuario.objects.filter(organizacao=request.user.organizacao).order_by('first_name')
    return render(request, 'empresas/equipe.html', {'usuarios': usuarios})

@login_required
def novo_membro(request):
    if request.user.cargo != 'dono':
        messages.error(request, 'Apenas o dono pode adicionar membros.')
        return redirect('empresas:equipe')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cargo = request.POST.get('cargo')
        
        if Usuario.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
        else:
            Usuario.objects.create_user(
                username=email, email=email, password=senha,
                first_name=nome, organizacao=request.user.organizacao, cargo=cargo
            )
            messages.success(request, f'Membro {nome} adicionado com sucesso!')
            return redirect('empresas:equipe')
            
    return render(request, 'empresas/form_membro.html')

@login_required
def remover_membro(request, pk):
    if request.user.cargo != 'dono':
        messages.error(request, 'Apenas o dono pode remover membros.')
        return redirect('empresas:equipe')
        
    membro = get_object_or_404(Usuario, pk=pk, organizacao=request.user.organizacao)
    if membro == request.user:
        messages.error(request, 'Você não pode remover a si mesmo.')
    else:
        membro.delete()
        messages.success(request, 'Membro removido.')
    return redirect('empresas:equipe')


@login_required
def editar_membro(request, pk):
    if request.user.cargo != 'dono':
        messages.error(request, 'Apenas o dono pode editar membros.')
        return redirect('empresas:equipe')
        
    membro = get_object_or_404(Usuario, pk=pk, organizacao=request.user.organizacao)
    
    if request.method == 'POST':
        membro.first_name = request.POST.get('nome')
        senha = request.POST.get('senha')
        if senha:
            membro.set_password(senha)
        if membro != request.user:
            membro.cargo = request.POST.get('cargo')
        membro.save()
        messages.success(request, 'Membro atualizado.')
        return redirect('empresas:equipe')
        
    return render(request, 'empresas/form_membro.html', {'membro': membro})

def assinatura(request):
    org = request.user.organizacao
    if not org:
        return redirect('empresas:cadastro')
        
    context = {
        'org': org,
        'dias_trial': 0
    }
    
    if org.status_assinatura == 'trial' and org.vencimento_trial:
        from django.utils import timezone
        delta = org.vencimento_trial - timezone.localdate()
        context['dias_trial'] = max(0, delta.days)
        
    return render(request, 'empresas/assinatura.html', context)

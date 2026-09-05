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
            return render(request, 'empresas/cadastro.html', {'empresa_nome': empresa_nome, 'nome': nome, 'email': email})
            
        if len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'empresas/cadastro.html', {'empresa_nome': empresa_nome, 'nome': nome, 'email': email})
            
        if Usuario.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return render(request, 'empresas/cadastro.html', {'empresa_nome': empresa_nome, 'nome': nome, 'email': email})

        ref_id = request.GET.get('ref')
        indicado_por = None
        if ref_id and ref_id.isdigit():
            indicado_por = Organizacao.objects.filter(pk=ref_id).first()

        try:
            with transaction.atomic():
                org = Organizacao.objects.create(nome=empresa_nome, indicado_por=indicado_por)
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
        
    # Lógica do Indique e Ganhe (B2B)
    eventos_concluidos = org.eventos.filter(status='concluido').count()
    pode_indicar = eventos_concluidos >= 5 or org.status_assinatura == 'ativa'
    link_indicacao = f"{request.scheme}://{request.get_host()}/empresas/cadastro/?ref={org.pk}"
    
    context = {
        'form': form,
        'eventos_concluidos': eventos_concluidos,
        'pode_indicar': pode_indicar,
        'link_indicacao': link_indicacao
    }
    return render(request, 'empresas/configuracoes.html', context)

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

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
def processar_assinatura(request):
    org = request.user.organizacao
    if org.asaas_subscription_id:
        messages.info(request, "Você já possui uma assinatura ativa ou em processamento.")
        return redirect('empresas:assinatura')
        
    from .asaas import criar_cliente, criar_assinatura
    
    # 1. Criar ou buscar Customer no Asaas
    if not org.asaas_customer_id:
        cliente_data = criar_cliente(org.nome, request.user.email, org.cnpj)
        if cliente_data and cliente_data.get('id'):
            org.asaas_customer_id = cliente_data['id']
            org.save()
        else:
            messages.error(request, "Erro ao conectar com o gateway de pagamento (Asaas). Verifique a API Key.")
            return redirect('empresas:assinatura')
            
    # 2. Criar Assinatura (ex: R$ 97,00 por mês)
    # Você pode parametrizar esse valor depois
    VALOR_PLANO = 97.00 
    
    assinatura_data = criar_assinatura(org.asaas_customer_id, VALOR_PLANO)
    if assinatura_data and assinatura_data.get('id'):
        org.asaas_subscription_id = assinatura_data['id']
        org.save()
        
        # Redireciona para o link de pagamento da fatura gerada
        # (O Asaas não retorna o invoiceUrl na assinatura, precisamos pegar da cobrança gerada,
        # mas por simplicidade, podemos apenas informar o usuário ou buscar a cobrança).
        messages.success(request, "Fatura gerada com sucesso! Verifique seu e-mail para pagamento.")
    else:
        messages.error(request, "Erro ao criar assinatura no gateway.")
        
    return redirect('empresas:assinatura')

@csrf_exempt
def webhook_asaas(request):
    """
    Recebe os pings do Asaas sobre o status do pagamento.
    Deve ser configurado no painel do Asaas apontando para: https://seudominio.com/empresas/webhook/asaas/
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = data.get('event')
            payment = data.get('payment', {})
            
            customer_id = payment.get('customer')
            subscription_id = payment.get('subscription')
            
            if not customer_id:
                return JsonResponse({"status": "ignored"})
                
            org = Organizacao.objects.filter(asaas_customer_id=customer_id).first()
            if not org:
                return JsonResponse({"status": "not_found"}, status=404)
                
            # Pagamento confirmado (PIX, Cartão ou Boleto pago)
            if event in ['PAYMENT_RECEIVED', 'PAYMENT_CONFIRMED']:
                org.status_assinatura = 'ativa'
                org.save()
                
            # Pagamento atrasado ou recusado
            elif event in ['PAYMENT_OVERDUE', 'PAYMENT_REFUNDED', 'PAYMENT_CHARGEBACK_REQUESTED']:
                org.status_assinatura = 'inadimplente'
                org.save()
                
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

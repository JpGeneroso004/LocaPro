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
            messages.success(request, f'Bem-vindo(a) ao Art.Tendas, {nome}! Sua conta da empresa {empresa_nome} foi criada.')
            return redirect('eventos:dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')

    return render(request, 'empresas/cadastro.html')

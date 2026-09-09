from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from . import views

app_name = 'inventario'

def em_construcao(request, **kwargs):
    messages.info(request, "⚙️ Funcionalidade em migração para a nova arquitetura SaaS. Estará disponível em breve!")
    return redirect('inventario:lista_equipamentos')

urlpatterns = [
    # Rotas Atuais (Fase 3 SaaS)
    path('equipamentos/', views.EquipamentoListView.as_view(), name='lista_equipamentos'),
    path('equipamentos/novo/', views.EquipamentoCreateView.as_view(), name='novo_equipamento'),
    
    # Aliases Legados (Evita NoReverseMatch no base.html)
    path('', views.EquipamentoListView.as_view(), name='painel'),
    
    # Rotas Fantasmas (Em Migração)
    path('equipamentos/<int:pk>/editar/', em_construcao, name='editar_equipamento'),
    path('equipamentos/<int:pk>/excluir/', em_construcao, name='excluir_equipamento'),
]

from django.urls import path
from . import views

app_name = 'empresas'
urlpatterns = [
    path('cadastro/', views.cadastro_locadora, name='cadastro'),
    path('configuracoes/', views.configuracoes_empresa, name='configuracoes'),
    path('configuracoes/excluir/', views.excluir_locadora, name='excluir_locadora'),
    path('equipe/', views.lista_equipe, name='equipe'),
    path('equipe/novo/', views.novo_membro, name='novo_membro'),
    path('equipe/editar/<int:pk>/', views.editar_membro, name='editar_membro'),
    path('equipe/remover/<int:pk>/', views.remover_membro, name='remover_membro'),
    path('financeiro/', views.dashboard_financeiro, name='financeiro'),
    path('assinatura/', views.assinatura, name='assinatura'),
    path('assinatura/processar/', views.processar_assinatura, name='processar_assinatura'),
    path('webhook/asaas/', views.webhook_asaas, name='webhook_asaas'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin'),
]

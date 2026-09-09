from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from . import views

app_name = 'eventos'

def em_construcao(request, **kwargs):
    messages.info(request, "⚙️ Funcionalidade em migração para a nova arquitetura SaaS. Estará disponível em breve!")
    return redirect('eventos:lista_eventos')

urlpatterns = [
    # Rotas Atuais (Fase 3 SaaS)
    path('', views.EventoListView.as_view(), name='lista_eventos'),
    path('novo/', views.EventoCreateView.as_view(), name='novo_evento'),
    
    # Aliases Legados (Evita NoReverseMatch em templates antigos)
    path('legado/lista/', views.EventoListView.as_view(), name='lista'),
    path('legado/novo/', views.EventoCreateView.as_view(), name='novo'),
    
    # Rotas Fantasmas (Em Migração para o Tenant Manager)
    path('<int:pk>/', em_construcao, name='detalhe'),
    path('<int:pk>/editar/', em_construcao, name='editar'),
    path('<int:pk>/excluir/', em_construcao, name='excluir'),
    path('<int:pk>/concluir/', em_construcao, name='concluir'),
    path('contrato/<int:pk>/aplicar-pontos/', em_construcao, name='aplicar_pontos'),
    path('contratos/', em_construcao, name='contratos_lista'),
    path('<int:evento_id>/gerar-contrato/', em_construcao, name='gerar_contrato'),
    path('contrato/<int:evento_id>/salvar-contrato/', em_construcao, name='salvar_contrato'),
    path('contrato/<int:contrato_id>/imprimir/', em_construcao, name='imprimir_contrato'),
    path('contratos/deletar/<int:contrato_id>/', em_construcao, name='deletar_contrato'),
    path('contratos/<int:contrato_id>/gerar-pdf-async/', em_construcao, name='gerar_pdf_async'),
    path('contrato/assinatura/<str:token>/', em_construcao, name='assinatura_cliente'),
    path('api/equipamentos-disponiveis/', em_construcao, name='equipamentos_disponiveis'),
]

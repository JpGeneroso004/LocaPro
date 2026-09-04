from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lista/', views.lista_eventos, name='lista'),
    path('<int:pk>/', views.detalhe_evento, name='detalhe'),
    path('novo/', views.novo_evento, name='novo'),
    path('<int:pk>/editar/', views.editar_evento, name='editar'),
    path('<int:pk>/excluir/', views.excluir_evento, name='excluir'),
    path('<int:pk>/concluir/', views.concluir_evento, name='concluir'),
    path('contrato/<int:pk>/aplicar-pontos/', views.aplicar_desconto_fidelidade, name='aplicar_pontos'),
    
    # Contratos
    path('contratos/', views.contratos_lista, name='contratos_lista'),
    path('<int:evento_id>/gerar-contrato/', views.gerar_contrato, name='gerar_contrato'),
    path('<int:evento_id>/salvar-contrato/', views.salvar_contrato, name='salvar_contrato'),
    path('contrato/<int:contrato_id>/imprimir/', views.imprimir_contrato, name='imprimir_contrato'),
    path('contrato/<int:contrato_id>/deletar/', views.deletar_contrato, name='deletar_contrato'),
    
    # API
    path('api/equipamentos-disponiveis/', views.obter_equipamentos_disponiveis, name='equipamentos_disponiveis'),
]

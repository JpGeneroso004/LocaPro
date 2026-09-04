from django.urls import path
from . import views

app_name = 'empresas'
urlpatterns = [
    path('cadastro/', views.cadastro_locadora, name='cadastro'),
    path('configuracoes/', views.configuracoes_empresa, name='configuracoes'),
    path('equipe/', views.lista_equipe, name='equipe'),
    path('equipe/novo/', views.novo_membro, name='novo_membro'),
    path('equipe/editar/<int:pk>/', views.editar_membro, name='editar_membro'),
    path('equipe/remover/<int:pk>/', views.remover_membro, name='remover_membro'),
    path('assinatura/', views.assinatura, name='assinatura'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin'),
]

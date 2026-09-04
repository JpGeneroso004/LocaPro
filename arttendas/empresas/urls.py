from django.urls import path
from . import views

app_name = 'empresas'
urlpatterns = [
    path('cadastro/', views.cadastro_locadora, name='cadastro'),
    path('configuracoes/', views.configuracoes_empresa, name='configuracoes'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin'),
]

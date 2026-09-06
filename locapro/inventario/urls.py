from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.painel_estoque, name='painel'),
    
    # Equipamentos
    path('novo/', views.novo_equipamento, name='novo_equipamento'),
    path('<int:pk>/editar/', views.editar_equipamento, name='editar_equipamento'),
    path('<int:pk>/excluir/', views.excluir_equipamento, name='excluir_equipamento'),
]

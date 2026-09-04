from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario, name='inventario'),
    # Tendas
    path('tenda/nova/',          views.nova_tenda,    name='nova_tenda'),
    path('tenda/<int:pk>/editar/', views.editar_tenda, name='editar_tenda'),
    path('tenda/<int:pk>/excluir/', views.excluir_tenda, name='excluir_tenda'),
    # Conjuntos de palco/piso
    path('palco/novo/',            views.novo_conjunto,    name='novo_conjunto'),
    path('palco/<int:pk>/editar/', views.editar_conjunto,  name='editar_conjunto'),
    path('palco/<int:pk>/excluir/', views.excluir_conjunto, name='excluir_conjunto'),
]

from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('equipamentos/', views.EquipamentoListView.as_view(), name='lista_equipamentos'),
    path('equipamentos/novo/', views.EquipamentoCreateView.as_view(), name='novo_equipamento'),
]

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Equipamento
from empresas.mixins import TenantRequiredMixin, TenantModelMixin

class EquipamentoListView(TenantRequiredMixin, ListView):
    model = Equipamento
    template_name = 'inventario/equipamento_list.html'
    context_object_name = 'equipamentos'
    # TenantManager já aplica o filtro transparente via ThreadLocal! Nenhuma query extra vaza.

class EquipamentoCreateView(TenantRequiredMixin, TenantModelMixin, CreateView):
    model = Equipamento
    template_name = 'inventario/equipamento_form.html'
    fields = ['nome', 'categoria', 'valor_diaria', 'tipo_rastreamento', 'quantidade_lote', 'status', 'observacoes']
    success_url = reverse_lazy('inventario:lista_equipamentos')
    # TenantModelMixin assegura form.instance.organizacao = request.user.organizacao

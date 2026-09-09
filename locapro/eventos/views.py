from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Evento
from empresas.mixins import TenantRequiredMixin, TenantModelMixin

class EventoListView(TenantRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'
    # TenantManager provê o isolamento transparente.

class EventoCreateView(TenantRequiredMixin, TenantModelMixin, CreateView):
    model = Evento
    template_name = 'eventos/evento_form.html'
    fields = ['nome', 'cliente_fidelidade', 'data_inicio', 'hora_inicio', 'data_fim', 'hora_fim', 'status']
    success_url = reverse_lazy('eventos:lista_eventos')
    # TenantModelMixin protege contra Mass Assignment / injeção de ID de outra locadora.

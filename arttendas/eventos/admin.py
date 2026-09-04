from django.contrib import admin
from .models import Evento
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'data_inicio', 'data_fim', 'status']
    list_filter = ['status']
    search_fields = ['nome', 'cliente']

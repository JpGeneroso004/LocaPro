from django.contrib import admin
from .models import Cliente, Evento, ItemEvento, Contrato

admin.site.register(Cliente)
admin.site.register(Evento)
admin.site.register(ItemEvento)
admin.site.register(Contrato)

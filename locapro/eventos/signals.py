from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Evento, ItemEvento
from inventario.models import Equipamento

def invalidar_cache_disponibilidade(organizacao_id):
    if organizacao_id:
        cache.add(f'inv_version_{organizacao_id}', 1) # caso não exista
        cache.incr(f'inv_version_{organizacao_id}')

@receiver(post_save, sender=Evento)
@receiver(post_delete, sender=Evento)
def limpar_cache_evento(sender, instance, **kwargs):
    invalidar_cache_disponibilidade(instance.organizacao_id)

@receiver(post_save, sender=ItemEvento)
@receiver(post_delete, sender=ItemEvento)
def limpar_cache_item(sender, instance, **kwargs):
    invalidar_cache_disponibilidade(instance.evento.organizacao_id)

@receiver(post_save, sender=Equipamento)
@receiver(post_delete, sender=Equipamento)
def limpar_cache_equipamento(sender, instance, **kwargs):
    invalidar_cache_disponibilidade(instance.organizacao_id)

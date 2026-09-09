import os
import django
import datetime
from django.utils import timezone

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from empresas.models import Organizacao, Usuario
from inventario.models import Equipamento, Patrimonio, CategoriaEquipamento
from eventos.models import Evento, ItemEvento, Cliente

def run():
    print("Limpando o banco de dados (Reset Geral)...")
    # Como não sobrescrevemos o delete() no nível do QuerySet, isso forçará um Hard Delete de tudo, limpando o banco para o teste.
    Usuario.objects.all().delete()
    ItemEvento.objects.all().delete()
    Patrimonio.objects.all().delete()
    Equipamento.objects.all().delete()
    CategoriaEquipamento.objects.all().delete()
    Evento.objects.all().delete()
    Cliente.objects.all().delete()
    Organizacao.objects.all().delete()

    print("Criando as Empresas (Tenants)...")
    locafesta = Organizacao.objects.create(
        nome="LocaFesta", 
        cor_primaria="#E11D48", # Rosa avermelhado
        segmento="brinquedos"
    )
    tendas_cia = Organizacao.objects.create(
        nome="Tendas & Cia", 
        cor_primaria="#0D9488", # Teal
        segmento="tendas"
    )

    print("Criando Usuários Donos...")
    Usuario.objects.create_user(
        username="dono@locafesta.com",
        email="dono@locafesta.com",
        password="admin123",
        first_name="João (LocaFesta)",
        organizacao=locafesta,
        cargo="dono"
    )
    Usuario.objects.create_user(
        username="dono@tendas.com",
        email="dono@tendas.com",
        password="admin123",
        first_name="Maria (Tendas)",
        organizacao=tendas_cia,
        cargo="dono"
    )

    print("Criando Catálogos Isolados...")
    cat_mobiliario, _ = CategoriaEquipamento.objects.get_or_create(nome="Mobiliário", organizacao=locafesta)
    cat_brinquedo, _ = CategoriaEquipamento.objects.get_or_create(nome="Brinquedos Infláveis", organizacao=locafesta)
    
    # LocaFesta - Lotes
    cadeiras = Equipamento.objects.create(
        nome="Cadeira de Plástico Branca",
        categoria=cat_mobiliario,
        valor_diaria=2.50,
        tipo_rastreamento="lote",
        quantidade_lote=200,
        organizacao=locafesta
    )
    mesas = Equipamento.objects.create(
        nome="Mesa de Plástico Branca",
        categoria=cat_mobiliario,
        valor_diaria=10.00,
        tipo_rastreamento="lote",
        quantidade_lote=50,
        organizacao=locafesta
    )
    Equipamento.objects.create(
        nome="Toalha de Mesa Branca (G)",
        categoria=cat_mobiliario,
        valor_diaria=5.00,
        tipo_rastreamento="lote",
        quantidade_lote=50,
        organizacao=locafesta
    )
    
    # LocaFesta - Serializado
    pula_pula = Equipamento.objects.create(
        nome="Pula-Pula Castelo 3x3m",
        categoria=cat_brinquedo,
        valor_diaria=150.00,
        tipo_rastreamento="serializado",
        organizacao=locafesta
    )
    # Cadastrando as 2 unidades físicas do pula-pula
    Patrimonio.objects.create(equipamento=pula_pula, numero_serie_ou_tag="PP-001 (Novo)", status="disponivel", organizacao=locafesta)
    Patrimonio.objects.create(equipamento=pula_pula, numero_serie_ou_tag="PP-002 (Remendado)", status="disponivel", organizacao=locafesta)
    
    # Tendas & Cia
    cat_tenda, _ = CategoriaEquipamento.objects.get_or_create(nome="Tendas Pesadas", organizacao=tendas_cia)
    Equipamento.objects.create(
        nome="Tenda Piramidal 5x5m",
        categoria=cat_tenda,
        valor_diaria=300.00,
        tipo_rastreamento="lote",
        quantidade_lote=10,
        organizacao=tendas_cia
    )
    Equipamento.objects.create(
        nome="Tenda Sanfonada 3x3m",
        categoria=cat_tenda,
        valor_diaria=120.00,
        tipo_rastreamento="lote",
        quantidade_lote=20,
        organizacao=tendas_cia
    )

    print("Criando Agendamento Crítico (Teste de Overbooking)...")
    cliente = Cliente.objects.create(
        nome="Juliana Silva",
        email="juliana@exemplo.com",
        organizacao=locafesta
    )
    
    data_inicio = timezone.localdate()
    data_fim = data_inicio + datetime.timedelta(days=2)
    
    evento = Evento.objects.create(
        nome="Festa de Aniversário - 100 Convidados",
        cliente_fidelidade=cliente,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status="em_andamento",
        organizacao=locafesta
    )
    
    # Ocupando 100 cadeiras (restarão 100 disponíveis) e 25 mesas (restarão 25)
    ItemEvento.objects.create(evento=evento, equipamento=cadeiras, quantidade=100, organizacao=locafesta, preco_fechado=250.00)
    ItemEvento.objects.create(evento=evento, equipamento=mesas, quantidade=25, organizacao=locafesta, preco_fechado=250.00)

    print("\nSeed executado com sucesso!")
    print("--------------------------------------------------")
    print("Credenciais de Teste:")
    print("1. Empresa: LocaFesta")
    print("   Login: dono@locafesta.com")
    print("   Senha: admin123")
    print("   Estoque: 100 cadeiras disponíveis (100 em uso).")
    print()
    print("2. Empresa: Tendas & Cia")
    print("   Login: dono@tendas.com")
    print("   Senha: admin123")
    print("   Estoque: Isolado (Verá apenas Tendas).")
    print("--------------------------------------------------")

if __name__ == '__main__':
    run()

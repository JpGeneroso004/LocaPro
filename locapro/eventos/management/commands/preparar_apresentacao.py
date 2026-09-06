from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from empresas.models import Organizacao
from inventario.models import Tenda, ConjuntoPalco
from eventos.models import Evento, Cliente, Contrato
import random

Usuario = get_user_model()

class Command(BaseCommand):
    help = "Gera dados lindos para apresentação a investidores"

    def handle(self, *args, **kwargs):
        self.stdout.write("Preparando a Versão Definitiva para o Investidor...")

        # 1. Cria a Organização Padrão
        org, _ = Organizacao.objects.get_or_create(
            nome="LocaPro Global",
            defaults={
                "cnpj": "12.345.678/0001-99",
                "cidade": "São Paulo",
                "estado": "SP",
                "plano": "premium",
                "meses_pagos": 12,
                "status_assinatura": "ativa",
                "chave_pix": "contato@locapro.com.br"
            }
        )
        org.save()

        # 2. Cria Usuário Dono
        if not Usuario.objects.filter(username="ceo@locapro.com").exists():
            Usuario.objects.create_superuser("ceo@locapro.com", "ceo@locapro.com", "investimento123", organizacao=org, cargo="dono", first_name="CEO")

        # 3. Limpa dados antigos da org para não duplicar
        Tenda.objects.filter(organizacao=org).delete()
        ConjuntoPalco.objects.filter(organizacao=org).delete()
        Evento.objects.filter(organizacao=org).delete()
        Cliente.objects.filter(organizacao=org).delete()

        # 4. Cria Inventário Farto
        tendas = []
        for i in range(1, 9):
            tendas.append(Tenda.objects.create(organizacao=org, codigo=f"T10x10-{i}", tamanho="10x10", tipo="piramidal", status="ativo"))
        for i in range(1, 6):
            tendas.append(Tenda.objects.create(organizacao=org, codigo=f"T5x5-{i}", tamanho="5x5", tipo="chapeu_bruxa", status="ativo"))
        
        palcos = []
        palcos.append(ConjuntoPalco.objects.create(organizacao=org, nome="Palco Principal 20m", quantidade_placas=40, status="ativo"))
        palcos.append(ConjuntoPalco.objects.create(organizacao=org, nome="Piso Pista de Dança", quantidade_placas=20, status="ativo"))

        # 5. Cria Clientes
        clientes = []
        nomes = ["Tech Summit Brasil", "Casamento de Luxo", "Festival de Inverno", "Feira do Empreendedor", "Prefeitura de SP"]
        for nome in nomes:
            clientes.append(Cliente.objects.create(organizacao=org, nome=nome, telefone="11999999999", email="contato@evento.com"))

        # 6. Cria Eventos (Mês Atual para dar volume no BI)
        hoje = timezone.localdate()
        status_choices = ["concluido", "em_andamento", "agendado"]
        
        for i in range(12):
            cliente = random.choice(clientes)
            dias_offset = random.randint(-15, 15)
            data_ini = hoje + timedelta(days=dias_offset)
            data_fim = data_ini + timedelta(days=random.randint(1, 3))
            
            st = "concluido" if dias_offset < 0 else "agendado"
            if dias_offset == 0: st = "em_andamento"

            evento = Evento.objects.create(
                organizacao=org,
                nome=f"Evento: {cliente.nome}",
                cliente_fidelidade=cliente,
                rua="Avenida Paulista", numero=str(random.randint(100, 2000)), setor="Bela Vista", cidade="São Paulo",
                data_inicio=data_ini, data_fim=data_fim,
                status=st,
                latitude="-23.5505", longitude="-46.6333"
            )
            
            # Adiciona tendas
            tendas_evento = random.sample(tendas, random.randint(1, 3))
            evento.tendas.set(tendas_evento)
            if random.choice([True, False]):
                evento.conjuntos.add(random.choice(palcos))
                
            # Cria contrato com valor alto
            Contrato.objects.create(
                evento=evento,
                organizacao=org,
                contratante_nome=cliente.nome,
                contratante_cpf_cnpj="00.000.000/0001-00",
                contratante_telefone="11999999999",
                endereco_montagem="Avenida Paulista, SP",
                valor_total=random.randint(4500, 15000),
                sinal=1000,
                forma_pagamento="PIX"
            )

        self.stdout.write(self.style.SUCCESS("Ambiente de Apresentacao gerado com sucesso!"))
        self.stdout.write(self.style.WARNING("Login: ceo@locapro.com | Senha: investimento123"))


import requests
import datetime
from django.conf import settings
from django.utils import timezone

def get_headers():
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": getattr(settings, 'ASAAS_API_KEY', '')
    }

def get_base_url():
    # Padrão é Sandbox para testes, pode ser mudado no .env
    return getattr(settings, 'ASAAS_URL', 'https://sandbox.asaas.com/api/v3')

def criar_cliente(nome, email, cpf_cnpj=None):
    url = f"{get_base_url()}/customers"
    payload = {
        "name": nome,
        "email": email,
    }
    if cpf_cnpj:
        payload["cpfCnpj"] = cpf_cnpj
        
    response = requests.post(url, json=payload, headers=get_headers())
    if response.status_code in [200, 201]:
        return response.json()
    return None

def criar_assinatura(customer_id, valor, ciclo="MONTHLY", descricao="Assinatura LocaPro SaaS"):
    url = f"{get_base_url()}/subscriptions"
    vencimento = timezone.localdate() + datetime.timedelta(days=1)
    
    payload = {
        "customer": customer_id,
        "billingType": "UNDEFINED", # Permite que o cliente escolha PIX, Cartão ou Boleto
        "value": valor,
        "nextDueDate": vencimento.strftime("%Y-%m-%d"),
        "cycle": ciclo,
        "description": descricao
    }
    
    response = requests.post(url, json=payload, headers=get_headers())
    if response.status_code in [200, 201]:
        return response.json()
    return None

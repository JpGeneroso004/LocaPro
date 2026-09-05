import os
from google import genai
from google.genai import types
from django.conf import settings
from .models import MensagemWhatsApp
from inventario.models import Tenda

def enviar_mensagem_whatsapp(telefone, texto, config):
    """
    Stub para envio da mensagem de volta para o cliente via API Oficial do WhatsApp Cloud.
    Na produção, esta função usará requests.post() apontando para graph.facebook.com/v17.0/...
    """
    import requests
    
    # Exemplo Estrutural da API Oficial do WhatsApp:
    '''
    url = f"https://graph.facebook.com/v17.0/{config.numero_whatsapp}/messages"
    headers = {
        "Authorization": f"Bearer {config.api_key_whatsapp}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=payload)
    '''
    # Como não temos a API Key real, apenas printamos para log (o Uptime Kuma pode ignorar isso)
    print(f"[ZAP-BOT] Enviando para {telefone}: {texto}")
    return True


def gerar_resposta_ia(org, telefone_cliente, mensagem_recebida):
    """
    Função principal que orquestra o cérebro do Bot.
    """
    config = org.config_ia
    
    if not config.bot_ativo or not config.api_key_llm:
        return None
        
    # 1. Salva a mensagem recebida no histórico
    MensagemWhatsApp.objects.create(
        organizacao=org,
        telefone_cliente=telefone_cliente,
        mensagem=mensagem_recebida,
        is_bot=False
    )
    
    # 2. Resgata o histórico recente (Memória de Curto Prazo) para contexto
    historico = MensagemWhatsApp.objects.filter(
        organizacao=org, 
        telefone_cliente=telefone_cliente
    ).order_by('-criado_em')[:10]
    
    historico = reversed(historico) # Do mais antigo pro mais novo (dentro dos últimos 10)
    
    # 3. Puxa os dados reais da Empresa (Estoque)
    tendas = Tenda.objects.filter(organizacao=org)
    contexto_estoque = "Catálogo de Tendas:\n"
    for t in tendas:
        contexto_estoque += f"- {t.tamanho} (Qtd: {t.quantidade_total}) - Preço aprox: R${t.valor_diaria}\n"
    
    # 4. Constrói o System Prompt (Injeção da Personalidade + Conhecimento de Negócio)
    system_instruction = f"""
Você é o assistente virtual '{config.nome_assistente}' da empresa {org.nome}.
Sua personalidade: {config.prompt_personalidade}

REGRA 1: Seja extremamente conciso. É o WhatsApp, não mande textos longos.
REGRA 2: Você vende locação de tendas e estruturas. Tente convencer o cliente a fechar o aluguel.
REGRA 3: Quando ele perguntar preço, use a base de dados abaixo. Nunca invente preços.

DADOS DA EMPRESA:
{contexto_estoque}
"""

    # 5. Configura e chama o Google Gemini 2.0 Flash (Mais rápido e barato para chat)
    try:
        client = genai.Client(api_key=config.api_key_llm)
        
        # Constrói o array de conversas no formato esperado pelo Gemini
        contents = []
        for msg in historico:
            role = 'model' if msg.is_bot else 'user'
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg.mensagem)])
            )
            
        # Gera a resposta
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7, # Foco em conversão sem alucinação
            )
        )
        
        resposta_texto = response.text
        
        # 6. Salva a resposta do Bot no banco e envia
        MensagemWhatsApp.objects.create(
            organizacao=org,
            telefone_cliente=telefone_cliente,
            mensagem=resposta_texto,
            is_bot=True
        )
        
        enviar_mensagem_whatsapp(telefone_cliente, resposta_texto, config)
        return resposta_texto
        
    except Exception as e:
        print(f"[ERRO IA] Falha ao consultar LLM: {e}")
        return "Desculpe, estou passando por uma instabilidade. Por favor, aguarde que um atendente humano já vai te responder."

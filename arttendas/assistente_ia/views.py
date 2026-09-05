from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConfiguracaoIA, MensagemWhatsApp
import json

@csrf_exempt
def webhook_whatsapp(request, org_id):
    """
    Endpoint (Webhook) que receberá as mensagens do WhatsApp (Meta/Evolution API).
    """
    if request.method == 'GET':
        # Verificação de Webhook (Meta API)
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        config = ConfiguracaoIA.objects.filter(organizacao_id=org_id).first()
        if config and verify_token == config.webhook_token:
            return HttpResponse(challenge)
        return HttpResponse('Token Inválido', status=403)
        
    if request.method == 'POST':
        # Aqui a IA irá processar a mensagem recebida e enviar de volta
        try:
            payload = json.loads(request.body)
            # Logica estrutural de parsing (Meta API)
            
            # Navega no payload da Meta Cloud API para extrair número e texto
            # Formato oficial: payload['entry'][0]['changes'][0]['value']['messages'][0]
            entry = payload.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [])
            
            if not messages:
                # Pode ser apenas um status update (entregue/lido)
                return JsonResponse({"status": "ignorado"})
                
            msg = messages[0]
            telefone_cliente = msg.get('from')
            texto_recebido = msg.get('text', {}).get('body')
            
            if telefone_cliente and texto_recebido:
                # Dispara a inteligência artificial
                org = ConfiguracaoIA.objects.get(organizacao_id=org_id).organizacao
                from .bot import gerar_resposta_ia
                
                # O ideal num servidor em produção seria jogar isso no Celery (delay),
                # mas vamos invocar de forma síncrona/thread para manter arquitetura inicial simples
                import threading
                threading.Thread(target=gerar_resposta_ia, args=(org, telefone_cliente, texto_recebido)).start()
            
            return JsonResponse({"status": "recebido"})
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=400)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def painel_ia(request):
    if request.user.cargo != "dono":
        return redirect("eventos:dashboard")
    
    config, _ = ConfiguracaoIA.objects.get_or_create(
        organizacao=request.user.organizacao,
        defaults={
            "bot_ativo": False,
            "numero_whatsapp": "",
        }
    )
    
    if request.method == "POST":
        config.bot_ativo = request.POST.get("bot_ativo") == "on"
        config.numero_whatsapp = request.POST.get("numero_whatsapp")
        config.nome_assistente = request.POST.get("nome_assistente")
        config.prompt_personalidade = request.POST.get("prompt_personalidade")
        config.save()
        return redirect("assistente_ia:painel")
        
    return render(request, "assistente_ia/painel.html", {"config": config})


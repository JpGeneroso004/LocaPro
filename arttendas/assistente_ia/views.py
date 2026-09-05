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
            # Logica de parsing do payload do WhatsApp seria aqui...
            
            # Exemplo de salvamento de memória:
            # MensagemWhatsApp.objects.create(organizacao_id=org_id, telefone_cliente=telefone, mensagem=texto, is_bot=False)
            
            return JsonResponse({"status": "recebido"})
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=400)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)

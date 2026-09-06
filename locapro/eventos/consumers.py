import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ContratoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.contrato_id = self.scope['url_route']['kwargs']['contrato_id']
        self.group_name = f'contrato_{self.contrato_id}'

        # Entrar no grupo
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Sair do grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receber mensagem do grupo
    async def contrato_message(self, event):
        message = event['message']
        status = event.get('status', 'processing')
        url = event.get('url', '')

        # Enviar para o WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'url': url
        }))

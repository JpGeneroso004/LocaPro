from celery import shared_task
from django.core.files.base import ContentFile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Contrato
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

@shared_task
def gerar_pdf_contrato(contrato_id):
    try:
        contrato = Contrato.objects.get(pk=contrato_id)
        
        # Simulando uma tarefa pesada
        time.sleep(2)
        
        # Gerando PDF com ReportLab
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawString(100, 800, f"CONTRATO DE LOCAÇÃO - LOCAPRO")
        p.drawString(100, 780, f"Organização: {contrato.organizacao.nome if contrato.organizacao else 'N/A'}")
        p.drawString(100, 760, f"Cliente: {contrato.contratante_nome}")
        p.drawString(100, 740, f"Evento: {contrato.evento.nome}")
        p.drawString(100, 720, f"Valor Total: R$ {contrato.valor_total}")
        p.drawString(100, 700, f"Status da Assinatura: {contrato.status_assinatura}")
        p.showPage()
        p.save()
        
        buffer.seek(0)
        
        filename = f'contrato_{contrato_id}.pdf'
        contrato.pdf_file.save(filename, ContentFile(buffer.read()))
        contrato.save()
        
        # Notificar o canal via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'contrato_{contrato_id}',
            {
                'type': 'contrato_message',
                'message': 'PDF gerado com sucesso!',
                'status': 'done',
                'url': contrato.pdf_file.url
            }
        )
    except Exception as e:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'contrato_{contrato_id}',
            {
                'type': 'contrato_message',
                'message': f'Erro ao gerar PDF: {str(e)}',
                'status': 'error'
            }
        )

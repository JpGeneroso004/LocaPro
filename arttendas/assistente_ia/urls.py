from django.urls import path
from . import views

app_name = "assistente_ia"

urlpatterns = [
    path("", views.painel_ia, name="painel"),
    path("webhook/<int:org_id>/", views.webhook_whatsapp, name="webhook_whatsapp"),
]

from django.urls import path
from . import views

app_name = "assistente_ia"

urlpatterns = [
    path("webhook/<int:org_id>/", views.webhook_whatsapp, name="webhook_whatsapp"),
]

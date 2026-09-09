from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('eventos/', views.EventoListView.as_view(), name='lista_eventos'),
    path('eventos/novo/', views.EventoCreateView.as_view(), name='novo_evento'),
]

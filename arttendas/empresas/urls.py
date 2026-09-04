from django.urls import path
from . import views

app_name = 'empresas'
urlpatterns = [
    path('cadastro/', views.cadastro_locadora, name='cadastro'),
]

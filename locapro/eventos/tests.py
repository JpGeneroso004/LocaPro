from django.test import TestCase
from django.contrib.auth import get_user_model
from empresas.models import Organizacao
from eventos.models import Evento, Cliente, Contrato
from datetime import date, timedelta

User = get_user_model()

class EventosMultiTenantTestCase(TestCase):
    def setUp(self):
        self.org_a = Organizacao.objects.create(nome="Alpha", cnpj="11111111111111")
        self.user_a = User.objects.create_user(username="alpha2", email="alpha@test.com", password="pwd")
        self.user_a.organizacao = self.org_a
        self.user_a.save()
        
        self.org_b = Organizacao.objects.create(nome="Beta", cnpj="22222222222222")
        self.user_b = User.objects.create_user(username="beta2", email="beta@test.com", password="pwd")
        self.user_b.organizacao = self.org_b
        self.user_b.save()

        self.cliente_a = Cliente.objects.create(
            organizacao=self.org_a, 
            nome="Cliente Alpha"
        )
        self.cliente_b = Cliente.objects.create(
            organizacao=self.org_b, 
            nome="Cliente Beta"
        )

        hoje = date.today()
        amanha = hoje + timedelta(days=1)

        self.evento_a = Evento.objects.create(
            organizacao=self.org_a,
            cliente=self.cliente_a,
            nome="Festa Alpha",
            data_inicio=hoje,
            data_fim=amanha,
            status='agendado'
        )
        
        self.evento_b = Evento.objects.create(
            organizacao=self.org_b,
            cliente=self.cliente_b,
            nome="Casamento Beta",
            data_inicio=hoje,
            data_fim=amanha,
            status='agendado'
        )

    def test_eventos_lista_isolation(self):
        """Test that User A only sees Events from Org A."""
        self.client.login(username="alpha2", email="alpha@test.com", password="pwd")
        response = self.client.get('/eventos/lista/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Festa Alpha")
        self.assertNotContains(response, "Casamento Beta")

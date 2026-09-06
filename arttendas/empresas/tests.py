from django.test import TestCase
from django.contrib.auth import get_user_model
from empresas.models import Organizacao

User = get_user_model()

class MultiTenantSecurityTestCase(TestCase):
    def setUp(self):
        # Empresa A
        self.org_a = Organizacao.objects.create(
            nome="Locadora Alpha",
            cnpj="11111111111111"
        )
        self.user_a = User.objects.create_user(
            username="alpha", email="alpha@teste.com",
            password="password123"
        )
        self.user_a.organizacao = self.org_a
        self.user_a.save()

        # Empresa B
        self.org_b = Organizacao.objects.create(
            nome="Locadora Beta",
            cnpj="22222222222222"
        )
        self.user_b = User.objects.create_user(
            username="beta", email="beta@teste.com",
            password="password123"
        )
        self.user_b.organizacao = self.org_b
        self.user_b.save()

    def test_organizacao_isolation_on_login(self):
        """Test that a user is correctly linked to their organization and not others."""
        self.client.login(username="alpha", email="alpha@teste.com", password="password123")
        response = self.client.get('/empresas/configuracoes/')
        
        # Test if the context returns the correct organization
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Locadora Alpha")
        self.assertNotContains(response, "Locadora Beta")

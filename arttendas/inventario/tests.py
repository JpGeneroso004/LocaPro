from django.test import TestCase
from django.contrib.auth import get_user_model
from empresas.models import Organizacao
from inventario.models import CategoriaEquipamento, Equipamento

User = get_user_model()

class InventarioTestCase(TestCase):
    def setUp(self):
        self.org = Organizacao.objects.create(nome="TestOrg", cnpj="000")
        self.user = User.objects.create_user(username="testuser", email="test@org.com", password="pwd")
        self.user.organizacao = self.org
        self.user.save()
        
        self.categoria = CategoriaEquipamento.objects.create(
            organizacao=self.org, 
            nome="Tendas"
        )
        
        self.equip = Equipamento.objects.create(
            organizacao=self.org,
            categoria=self.categoria,
            nome="Tenda 5x5",
            quantidade_total=10
        )

    def test_painel_inventario(self):
        self.client.login(username="testuser", email="test@org.com", password="pwd")
        response = self.client.get('/inventario/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tenda 5x5")
        self.assertContains(response, "10")

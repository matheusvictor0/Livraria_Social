from django.test import TestCase
from ..models import Usuario

class UsuarioModelTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(
            nome="Maria",
            email="maria@test.com",
            senha="senha123",
            confirmado=False
        )

    def test_return_str(self):
        user = Usuario.objects.get(nome="Maria")
        self.assertEquals(user.__str__(), 'Maria')

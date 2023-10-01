from django.test import TestCase
from usuarios.models import Usuario
from django.urls import reverse
from hashlib import sha256

class UsuarioViewTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="Matheus",
            email="matheus@teste.com",
            senha=sha256("matheus12".encode()).hexdigest(),
            confirmado=True
        )

    def test_valida_login_view(self):
        data = {
            'email': 'matheus@teste.com',
            'senha': 'matheus12',
        }

        response = self.client.post(reverse('valida_login'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('usuario'), self.usuario.id)
        self.assertRedirects(response, reverse('home'))

    def test_solicitar_redefinicao_senha_view(self):
        data = {
            'email': 'matheus@teste.com',
        }

        response = self.client.post(reverse('solicitar_redefinicao_senha'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('solicitar_redefinicao_senha') + '?status=4')
        self.usuario.refresh_from_db()
        self.assertIsNotNone(self.usuario.token_confirmacao)
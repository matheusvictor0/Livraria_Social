from django.test import TestCase
import unittest
from django.urls import reverse
from usuarios.models import Usuario
from hashlib import sha256

class LoginTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome="Test User", 
                                              email="test@example.com", 
                                              senha=sha256(b'testpassword').hexdigest(), 
                                              confirmado=True)
        self.login_url = reverse('valida_login')
        

    def test_login_success(self):
        # Criação de uma solicitação POST simulada com dados válidos
        data = {'email': 'test@example.com', 'senha': 'testpassword'}
        response = self.client.post(self.login_url, data)

        # Verifica se o login foi bem-sucedido e redirecionou o usuário
        self.assertEqual(response.status_code, 302)
        # Verifica se o login foi bem-sucedido e redirecionou o usuário
        self.assertRedirects(response, '/livro/home/')  # Verifica se redirecionou para a página inicial após o login.

    def test_login_failure_invalid_credentials(self):
        # Criação de uma solicitação POST simulada com credenciais inválidas
        data = {'email': 'test@example.com', 'senha': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        # Verifica se o login falhou e redirecionou o usuário
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?status=1')  # Verifica se o status 1 foi adicionado à URL de redirecionamento.

    def test_login_failure_unconfirmed_user(self):
        # Configura o usuário como não confirmado
        self.usuario.confirmado = False
        self.usuario.save()

        # Criação de uma solicitação POST simulada com credenciais válidas
        data = {'email': 'test@example.com', 'senha': 'testpassword'}
        response = self.client.post(self.login_url, data)

        # Verifica se o login falhou devido ao usuário não confirmado
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/login/?status=2')  # Verifica se o status 2 foi adicionado à URL de redirecionamento.

  # Substitua "myapp" pelo nome real do seu aplicativo Django


if __name__ == '__main__':
    unittest.main()
import unittest
from django.urls import reverse
from usuarios.models import Usuario
from usuarios.views import valida_cadastro
from django.test.client import RequestFactory


class CadastroTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

#  Teste de Cadastro validando
    def test_cadastro_success(self):
        data = {
            'nome': 'Novo Usuário',
            'email': 'novo@example.com',
            'senha': 'password123',
            'senha_repeticao': 'password123',
        }
        
        request = self.factory.post(reverse('valida_cadastro'), data)
        response = valida_cadastro(request)
        
        # Verifica se o cadastro foi bem-sucedido e redirecionou o usuário para '/auth/cadastro/?status=0'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/cadastro/?status=0')

        # Verifica se o usuário foi criado no banco de dados
        self.assertTrue(Usuario.objects.filter(email=data['email']).exists())

    
    #Teste para email existindo
    def test_valida_cadastro_existing_email(self):
    # Criação de um usuário com o mesmo email no banco de dados
        Usuario.objects.create(nome='Existing User', email='usersuccess@example.com', senha='testpassword')

        data = {
            'nome': 'Usuario Teste',
            'email': 'usersuccess@example.com',
            'senha': 'testpassword123',
            'senha_repeticao': 'testpassword123',
        }
        request = self.factory.post(reverse('valida_cadastro'), data)
        response = valida_cadastro(request)

        # status=3 Usuário já existe no sistema
        self.assertEqual(response.status_code, 302)
        # Retorna o status 3
        self.assertEqual(response.url, '/auth/cadastro/?status=3')
        
        # Verifica se nenhum novo usuário foi criado no banco de dados
        self.assertTrue(Usuario.objects.filter(email='usersuccess@example.com').exists())
    
    #Teste para senhas que não coicidem
    def test_valida_cadastro_password_mismatch(self):
            # Criação de uma solicitação POST simulada com senhas que não coincidem
            data = {
                'nome': 'Pedro Afonso',
                'email': 'passwordtest@example.com',
                'senha': 'password1',
                'senha_repeticao': 'password2',
            }
            request = self.factory.post(reverse('valida_cadastro'), data)

            # Chama a função valida_cadastro com a solicitação simulada
            response = valida_cadastro(request)

            # status=5 (senhas não coincidem)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/auth/cadastro/?status=5')

            # Verifica se nenhum novo usuário foi criado no banco de dados
            self.assertFalse(Usuario.objects.filter(nome='Pedro Afonso').exists())

    #Teste para com tudo em branco
    def test_valida_cadastro_blank_fields(self):
            # Criação de uma solicitação POST simulada com campos em branco
            data = {
                'nome': '',
                'email': '',
                'senha': '',
                'senha_repeticao': '',
            }
            request = self.factory.post(reverse('valida_cadastro'), data)

            # Chama a função valida_cadastro com a solicitação simulada
            response = valida_cadastro(request)

            # Verifica se a resposta redireciona para a página de cadastro com status=1 (campos em branco)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/auth/cadastro/?status=1')

            # Verifica se nenhum novo usuário foi criado no banco de dados
            self.assertFalse(Usuario.objects.filter(nome='').exists())
        
    #Teste para senhas curtas
    def test_valida_cadastro_short_password(self):
        # Criação de uma solicitação POST simulada com uma senha curta
        data = {
            'nome': 'Short Password',
            'email': 'shortpassword@example.com',
            'senha': 'short',
            'senha_repeticao': 'short',
        }
        request = self.factory.post(reverse('valida_cadastro'), data)

        # Chama a função valida_cadastro com a solicitação simulada
        response = valida_cadastro(request)

        # Verifica se a resposta redireciona para a página de cadastro com status=2 (senha curta)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/cadastro/?status=2')

        # Verifica se nenhum novo usuário foi criado no banco de dados
        user_exists = Usuario.objects.filter(email='shortpassword@example.com').exists()
        self.assertFalse(user_exists)

if __name__ == '__main__':
    unittest.main()


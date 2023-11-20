import unittest
from unittest.mock import patch
from django.test import Client, RequestFactory
from django.urls import reverse
import requests
from livro.models import Livros
from livro.views import adicionar_livro, buscar_dados_livro, categoria, ver_livros
import usuarios.models 

class TestBuscarDadosLivro(unittest.TestCase):
    @patch('requests.get')
    def test_buscar_dados_livro_success(self, mock_get):
        # Configura o objeto de resposta simulada
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "volumeInfo": {
                        "title": "Título do Livro",
                        "authors": ["Autor do Livro"],
                        "imageLinks": {"thumbnail": "capa_url"},
                        "description": "Descrição do livro",
                        "categories": ["Ficção"],
                        "industryIdentifiers": [{"type": "ISBN_13", "identifier": "1234567890"}]
                    }
                }
            ]
        }

        # Chama a função para buscar dados do livro
        livros = buscar_dados_livro("Livro de Exemplo")

        # Verifica se os dados do livro foram retornados corretamente
        self.assertEqual(len(livros), 1)
        livro = livros[0]
        self.assertEqual(livro['titulo'], "Título do Livro")
        self.assertEqual(livro['autores'], "Autor do Livro")
        self.assertEqual(livro['capa_url'], "capa_url")
        self.assertEqual(livro['descricao'], "Descrição do livro")
        self.assertEqual(livro['genero'], "Ficção")
        self.assertEqual(livro['isbn'], "1234567890")

    @patch('requests.get')
    def test_buscar_dados_livro_no_items(self, mock_get):
        # Configura o objeto de resposta simulada sem "items"
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        # Chama a função para buscar dados do livro
        livros = buscar_dados_livro("Livro Inexistente")

        # Verifica se a lista de livros está vazia
        self.assertEqual(len(livros), 0)

    @patch('requests.get')
    def test_buscar_dados_livro_request_error(self, mock_get):
        # Simula um erro de solicitação
        mock_get.side_effect = requests.exceptions.RequestException("Erro na solicitação")

        # Chama a função para buscar dados do livro
        livros = buscar_dados_livro("Livro de Erro")


#Função barra_buscar

class TestBarraBuscar(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('livro.views.buscar_dados_livro')
    def test_barra_buscar_with_results(self, mock_buscar_dados_livro):
        # Simula o resultado da função buscar_dados_livro
        mock_buscar_dados_livro.return_value = [{'titulo': 'Livro 1'}, {'titulo': 'Livro 2'}]

        response = self.client.get(reverse('buscar'), {'termo_pesquisa': 'Harry Potter'})

        # Verifica se a resposta HTTP foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se os livros foram passados para o contexto do modelo
        self.assertEqual(len(response.context['livros']), 2)

    @patch('livro.views.buscar_dados_livro')
    def test_barra_buscar_without_results(self, mock_buscar_dados_livro):
        # Simula um cenário em que buscar_dados_livro não retorna resultados
        mock_buscar_dados_livro.return_value = []

        response = self.client.get(reverse('buscar'), {'termo_pesquisa': 'Não existente'})

        # Verifica se a resposta HTTP foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se a lista de livros no contexto está vazia
        self.assertEqual(len(response.context['livros']), 0)

    def test_barra_buscar_no_termo_pesquisa(self):
    # Faça uma solicitação GET para a view sem um termo de pesquisa
        response = self.client.get(reverse('buscar'))

    # Verifica se a resposta HTTP foi bem-sucedida
        self.assertEqual(response.status_code, 200)

    # Verifica o comprimento da lista de livros
        if response.context['livros'] is not None:
            self.assertEqual(len(response.context['livros']), 0)

    #Função de adicionar Livro

class TestAdicionarLivro(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('livro.views.buscar_dados_livro')
    def test_adicionar_livro_success(self, mock_buscar_dados_livro):
        # Simula o resultado da função buscar_dados_livro
        mock_buscar_dados_livro.return_value = [{
            'titulo': 'Livro de Teste',
            'autores': 'Autor de Teste',
            'capa_url': 'http://example.com/capa.jpg',
            'descricao': 'Descrição de Teste',
            'genero': 'Ficção Científica',
            'isbn': '1234567890'
        }]

        # Faz uma solicitação para adicionar o livro
        response = self.client.get(reverse('adicionar_livro', args=['1234567890']))

        # Verifica se a resposta HTTP foi bem-sucedida
        self.assertEqual(response.status_code, 302)  # Redirecionamento

        # Verifica se o livro foi adicionado ao banco de dados
        livro = Livros.objects.get(isbn='1234567890')
        self.assertEqual(livro.nome, 'Livro de Teste')
        self.assertEqual(livro.autor, 'Autor de Teste')
        self.assertEqual(livro.capa_url, 'http://example.com/capa.jpg')
        self.assertEqual(livro.descricao, 'Descrição de Teste')
        self.assertEqual(livro.genero, 'Ficção Científica')

    
#Função de Categorias

class CategoriaTest(unittest.TestCase):

    def setUp(self):
        # Configuração de dados de teste
        Livros.objects.create(isbn='12345678901232313123', nome='Livro A', autor='Autor A', capa_url='http://example.com', descricao='Descrição A', genero='Ficção Científica', avaliacao=4.5)
        Livros.objects.create(isbn='7890121231243123213', nome='Livro B', autor='Autor B', capa_url='http://example.com', descricao='Descrição B', genero='Ficção Científica', avaliacao=3.5)

        # Apaga os registros no banco de dados
        Livros.objects.filter(isbn='12345678901232313123').delete()
        Livros.objects.filter(isbn='7890121231243123213').delete()

    def test_categorias(self):
        result = categoria()

        # Verifica se a função retorna um conjunto (set) não vazio
        self.assertIsNotNone(result)
        self.assertIsInstance(result, set)
        self.assertTrue(result)

        # Verifica se as categorias retornadas estão corretas
        expected_categories = {"Ficção Científica", "Ficção Científica"}
        self.assertEqual(result, expected_categories)


#ver livros

if __name__ == '__main__':
    unittest.main()

from django.test import TestCase
from django.urls import reverse
from livro.models import Livros
from livro.views import Livros

class LivrosModelTestCase(TestCase):
    def setUp(self):
        # Criando um livro existente para testes
        Livros.objects.create(
            isbn='9781638351368',
            nome='Specification by Example',
            autor='Gojko Adzic',
            capa_url='http://books.google.com/books/content?id=fDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
            descricao='Test description',
            genero='Computers'
        )

    def test_livros_model_str(self):
        # Testa o método __str__ do modelo Livros
        livro = Livros.objects.get(isbn='9781638351368')
        self.assertEqual(str(livro), 'Specification by Example')

class LivrosViewsTestCase(TestCase):
    def test_barra_buscar_view(self):
         #Testa a view barra_buscar
        response = self.client.get(reverse('buscar'), {'termo_pesquisa': 'Specification by Example'})
        self.assertEqual(response.status_code, 200)  # Verifica se a página carrega corretamente
        self.assertContains(response, 'Specification by Example')  # Verifica se o livro de teste está na página

    def test_ver_livros_view(self):
        # Testa a view ver_livros
        livro = Livros.objects.create(
            isbn='9781638351368',
            nome='Specification by Example',
            autor='Gojko Adzic',
            capa_url='http://books.google.com/books/content?id=fDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
            descricao='Test description',
            genero='Computers'
        )
        response = self.client.get(reverse('ver_livros', args=[livro.isbn]))
        self.assertEqual(response.status_code, 200)  # Verifica se a página carrega corretamente
        self.assertContains(response, 'Specification by Example')  # Verifica se o livro de teste está na página

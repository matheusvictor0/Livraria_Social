import unittest
import requests

class TestGoogleBooksAPI(unittest.TestCase):
    def test_google_books_search(self):
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": "python"}
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, params=params, headers=headers)

        self.assertEqual(response.status_code, 200, "A resposta da API não retornou 200 OK")

        data = response.json()
        self.assertTrue("items" in data, "Nenhum item encontrado na resposta da API")

if __name__ == "__main__":
    unittest.main()

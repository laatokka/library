from django.test import TestCase, Client
from library.models import Book

class BookSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book1 = Book.objects.create(name="Harry Potter and the Philosopher's Stone", isbn="111", pages=100)
        self.book2 = Book.objects.create(name="The Hobbit", isbn="222", pages=200)
        self.book3 = Book.objects.create(name="1984", isbn="333", pages=300)

    def test_search_exact(self):
        response = self.client.get('/?search=The Hobbit')
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.context)
        self.assertIn(self.book2, response.context['books'])
        self.assertNotIn(self.book1, response.context['books'])

    def test_search_partial(self):
        response = self.client.get('/?search=Harry')
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.context)
        self.assertIn(self.book1, response.context['books'])
        self.assertNotIn(self.book2, response.context['books'])

    def test_search_wildcard_star(self):
        response = self.client.get('/?search=H*y')
        # Should match "Harry" part of "Harry Potter..."
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.context)
        self.assertIn(self.book1, response.context['books'])
        self.assertNotIn(self.book2, response.context['books'])

    def test_search_wildcard_question(self):
        response = self.client.get('/?search=1?84')
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.context)
        self.assertIn(self.book3, response.context['books'])
        self.assertNotIn(self.book1, response.context['books'])

    def test_search_no_results(self):
        response = self.client.get('/?search=Zorro')
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.context)
        self.assertEqual(len(response.context['books']), 0)

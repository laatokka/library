import pytest
from django.urls import reverse
from library.models import Book

@pytest.mark.django_db
class TestBookSearch:
    @pytest.fixture(autouse=True)
    def setup_books(self):
        Book.objects.create(name="Harry Potter", isbn="111", pages=100)
        Book.objects.create(name="The Hobbit", isbn="222", pages=100)
        Book.objects.create(name="Cat in the Hat", isbn="333", pages=100)
        Book.objects.create(name="Catch-22", isbn="444", pages=100)
        Book.objects.create(name="(Special) Book", isbn="555", pages=100)

    def test_basic_search(self, client):
        """Test basic substring search (default behavior of iregex without anchors)."""
        response = client.get(reverse('index'), {'search': 'Harry'})
        assert response.status_code == 200
        books = list(response.context['books'])
        assert len(books) == 1
        assert books[0].name == "Harry Potter"

        response = client.get(reverse('index'), {'search': 'Cat'})
        assert response.status_code == 200
        books = list(response.context['books'])
        assert len(books) == 2  # Cat in the Hat, Catch-22
        names = [b.name for b in books]
        assert "Cat in the Hat" in names
        assert "Catch-22" in names

    def test_wildcard_asterisk(self, client):
        """Test wildcard * matching any sequence of characters."""
        # 'H*r' should match 'Harry Potter' (H...r...)
        response = client.get(reverse('index'), {'search': 'H*r'})
        assert response.status_code == 200
        books = list(response.context['books'])
        names = [b.name for b in books]
        assert "Harry Potter" in names
        assert "The Hobbit" not in names # Hobbit doesn't match H*r (starts with T)

    def test_wildcard_question_mark(self, client):
        """Test wildcard ? matching exactly one character."""
        # 'C?t' should match 'Cat' and 'Cat' in Catch-22
        response = client.get(reverse('index'), {'search': 'C?t'})
        assert response.status_code == 200
        books = list(response.context['books'])
        names = [b.name for b in books]
        assert "Cat in the Hat" in names
        assert "Catch-22" in names

    def test_special_characters_escaped(self, client):
        """Test that regex special characters are treated as literals."""
        # Search for '(Special)' - parens should be escaped and not treated as regex group
        response = client.get(reverse('index'), {'search': '(Special)'})
        assert response.status_code == 200
        books = list(response.context['books'])
        assert len(books) == 1
        assert books[0].name == "(Special) Book"

    def test_mixed_wildcards(self, client):
        """Test mixing wildcards."""
        # '*b?t' -> matches 'The Hobbit' (end with b.t -> bit)
        response = client.get(reverse('index'), {'search': '*b?t'})
        assert response.status_code == 200
        books = list(response.context['books'])
        names = [b.name for b in books]
        assert "The Hobbit" in names

    def test_no_results(self, client):
        response = client.get(reverse('index'), {'search': 'NonExistent'})
        assert response.status_code == 200
        books = list(response.context['books'])
        assert len(books) == 0

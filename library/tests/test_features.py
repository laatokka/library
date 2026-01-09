
import pytest
from django.urls import reverse
from library.models import Book, Loan, UserData
from django.utils import timezone
import json

@pytest.mark.django_db
def test_book_genre_field():
    book = Book.objects.create(name="Test Book", isbn="1234567890123", pages=100, genre="Sci-Fi")
    assert book.genre == "Sci-Fi"

@pytest.mark.django_db
def test_user_data_creation(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    # UserData should be created automatically in the view, but here we can create it manually
    user_data = UserData.objects.create(user=user)
    assert user_data.user == user

@pytest.mark.django_db
def test_favorite_genre_calculation(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    book1 = Book.objects.create(name="Book 1", isbn="111", pages=100, genre="Sci-Fi")
    book2 = Book.objects.create(name="Book 2", isbn="222", pages=100, genre="Sci-Fi")
    book3 = Book.objects.create(name="Book 3", isbn="333", pages=100, genre="Fantasy")

    Loan.objects.create(user=user, book=book1)
    Loan.objects.create(user=user, book=book2)
    Loan.objects.create(user=user, book=book3)

    response = client.get(reverse('account'))
    assert response.status_code == 200
    assert response.context['favorite_genre'] == "Sci-Fi"

@pytest.mark.django_db
def test_download_user_data(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    book1 = Book.objects.create(name="Book 1", isbn="111", pages=100, genre="Sci-Fi")
    book2 = Book.objects.create(name="Book 2", isbn="222", pages=100, genre="Fantasy")

    Loan.objects.create(user=user, book=book1)

    # Mark book2 as read in UserData
    user_data = UserData.objects.create(user=user)
    user_data.read_books.add(book2)

    response = client.get(reverse('download_user_data'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    data = json.loads(response.content)
    assert data['username'] == 'testuser'
    assert len(data['loan_history']) == 1
    assert data['loan_history'][0]['book'] == "Book 1"
    assert data['loan_history'][0]['genre'] == "Sci-Fi"
    assert "Book 2" in data['read_books']
    assert data['favorite_genre'] == "Sci-Fi"

@pytest.mark.django_db
def test_toggle_book_read(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    book = Book.objects.create(name="Book 1", isbn="111", pages=100, genre="Sci-Fi")

    # Mark as read
    response = client.post(reverse('toggle_book_read', args=[book.id]))
    assert response.status_code == 302

    user_data = UserData.objects.get(user=user)
    assert book in user_data.read_books.all()

    # Unmark as read
    response = client.post(reverse('toggle_book_read', args=[book.id]))
    assert response.status_code == 302

    assert book not in user_data.read_books.all()

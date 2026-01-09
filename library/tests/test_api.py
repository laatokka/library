import json
import pytest
from django.urls import reverse
from library.models import Book, Loan

@pytest.mark.django_db
def test_loan_book_unauthenticated(client):
    url = reverse('loan_book')
    response = client.post(url, data={'nfc_tag': '123'}, content_type='application/json')
    # Should redirect to login or return 401/403 depending on configuration.
    # @login_required typically redirects to login page.
    assert response.status_code == 302

@pytest.mark.django_db
def test_loan_book_success(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    book = Book.objects.create(name="Test Book", isbn="1234567890123", pages=100, nfc_tag="test_nfc_123")

    url = reverse('loan_book')
    response = client.post(url, data={'nfc_tag': 'test_nfc_123'}, content_type='application/json')

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Loan created successfully'
    assert data['book'] == 'Test Book'

    assert Loan.objects.count() == 1
    loan = Loan.objects.first()
    assert loan.user == user
    assert loan.book == book
    assert loan.return_date is None

@pytest.mark.django_db
def test_loan_book_not_found(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    url = reverse('loan_book')
    response = client.post(url, data={'nfc_tag': 'non_existent'}, content_type='application/json')

    assert response.status_code == 404
    assert response.json()['error'] == 'Book not found'

@pytest.mark.django_db
def test_loan_book_already_loaned(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    book = Book.objects.create(name="Test Book", isbn="1234567890123", pages=100, nfc_tag="test_nfc_123")
    Loan.objects.create(user=user, book=book)

    url = reverse('loan_book')
    response = client.post(url, data={'nfc_tag': 'test_nfc_123'}, content_type='application/json')

    assert response.status_code == 400
    assert response.json()['error'] == 'Book is already on loan'

    # Should still only be 1 loan
    assert Loan.objects.count() == 1

@pytest.mark.django_db
def test_loan_book_invalid_json(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    url = reverse('loan_book')
    response = client.post(url, data='invalid json', content_type='application/json')

    assert response.status_code == 400
    assert response.json()['error'] == 'Invalid JSON'

@pytest.mark.django_db
def test_loan_book_missing_tag(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.force_login(user)

    url = reverse('loan_book')
    response = client.post(url, data={}, content_type='application/json')

    assert response.status_code == 400
    assert response.json()['error'] == 'nfc_tag is required'

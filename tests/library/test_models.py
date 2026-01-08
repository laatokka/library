from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from library.models import User, Book, Loan
from datetime import date

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='password123',
            address='123 Main St',
            phone_number='555-0199'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.address, '123 Main St')
        self.assertEqual(user.phone_number, '555-0199')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(str(user), 'testuser')

    def test_user_missing_fields(self):
        # address and phone_number are optional
        user = User.objects.create_user(username='testuser2', password='password123')
        self.assertIsNone(user.address)
        self.assertIsNone(user.phone_number)

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name='Test Book',
            isbn='1234567890123',
            pages=100
        )

    def test_book_creation(self):
        self.assertEqual(self.book.name, 'Test Book')
        self.assertEqual(self.book.isbn, '1234567890123')
        self.assertEqual(self.book.pages, 100)
        self.assertEqual(str(self.book), 'Test Book')

    def test_unique_isbn(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                name='Another Book',
                isbn='1234567890123', # Same ISBN
                pages=200
            )

    def test_isbn_max_length(self):
        book = Book(
            name='Long ISBN Book',
            isbn='1' * 14, # 14 chars, max is 13
            pages=300
        )
        with self.assertRaises(ValidationError):
            book.full_clean()

class LoanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loanuser', password='password')
        self.book = Book.objects.create(name='Loan Book', isbn='1111111111111', pages=150)

    def test_loan_creation(self):
        loan = Loan.objects.create(user=self.user, book=self.book)
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.book, self.book)
        self.assertIsNotNone(loan.loan_date)
        self.assertIsNone(loan.return_date)
        self.assertEqual(str(loan), f"{self.user.username} - {self.book.name}")

    def test_loan_return_date(self):
        loan = Loan.objects.create(user=self.user, book=self.book, return_date=date(2023, 12, 31))
        self.assertEqual(loan.return_date, date(2023, 12, 31))

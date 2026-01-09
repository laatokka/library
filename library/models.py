from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Keeping standard AbstractUser fields for name (first_name, last_name)
    # but we can access full name via get_full_name()

    def __str__(self):
        return self.username

class Book(models.Model):
    name = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    BOOK_TYPES = [
        ('fantasy', 'Fantasy'),
        ('science', 'Science'),
        ('romance', 'Romance'),
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        ('history', 'History'),
        ('biography', 'Biography'),
    ]
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES, default='fantasy')
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='data')
    read_books = models.ManyToManyField(Book, related_name='read_by_users', blank=True)

    def __str__(self):
        return f"Data for {self.user.username}"

    def get_favorite_genre(self):
        loans = self.user.loans.select_related('book').all()
        genres = [loan.book.genre for loan in loans if loan.book.genre]
        if genres:
            return max(set(genres), key=genres.count)
        return None

from django.db import models
from .user import User
from .book import Book

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

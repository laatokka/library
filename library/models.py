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

    def __str__(self):
        return self.name

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"

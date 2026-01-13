from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    nfc_tag = models.CharField(max_length=255, unique=True, null=True, blank=True)
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
    location = models.ForeignKey('library.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    author = models.ForeignKey('library.Author', on_delete=models.CASCADE, related_name='books', null=True, blank=True)

    def __str__(self):
        return self.name

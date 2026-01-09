from django.shortcuts import render
from .models import Book

def index(request):
    book_type = request.GET.get('type')
    if book_type:
        books = Book.objects.filter(book_type=book_type)
    else:
        books = Book.objects.all()

    return render(request, 'index.html', {
        'books': books,
        'book_types': Book.BOOK_TYPES,
        'selected_type': book_type,
    })

from django.shortcuts import render
from .models import Book
import re

def index(request):
    search_query = request.GET.get('search')
    if search_query:
        # Escape special regex characters
        pattern = re.escape(search_query)
        # Replace escaped wildcards with regex equivalents
        pattern = pattern.replace(r'\*', '.*').replace(r'\?', '.')
        books = Book.objects.filter(name__iregex=pattern)
    else:
        books = Book.objects.all()

    return render(request, 'index.html', {'books': books})

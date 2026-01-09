from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import UserData, Book
from django.db.models import Count
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')

@login_required
def account_view(request):
    user = request.user
    # Ensure UserData exists
    user_data, created = UserData.objects.get_or_create(user=user)

    loans = user.loans.select_related('book').order_by('-loan_date')
    read_book_ids = set(user_data.read_books.values_list('id', flat=True))

    context = {
        'customer_since': user.date_joined,
        'loans': loans,
        'favorite_genre': user_data.get_favorite_genre(),
        'read_book_ids': read_book_ids,
    }
    return render(request, 'account.html', context)

@login_required
def toggle_book_read(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_data, _ = UserData.objects.get_or_create(user=request.user)

        if book in user_data.read_books.all():
            user_data.read_books.remove(book)
        else:
            user_data.read_books.add(book)

    return redirect('account')

@login_required
def download_user_data(request):
    user = request.user
    user_data, created = UserData.objects.get_or_create(user=user)

    loans = user.loans.select_related('book').order_by('-loan_date')
    loan_history = []

    for loan in loans:
        loan_info = {
            'book': loan.book.name,
            'isbn': loan.book.isbn,
            'genre': loan.book.genre,
            'loan_date': str(loan.loan_date),
            'return_date': str(loan.return_date) if loan.return_date else None
        }
        loan_history.append(loan_info)

    read_books = [book.name for book in user_data.read_books.all()]

    data = {
        'username': user.username,
        'email': user.email,
        'date_joined': str(user.date_joined),
        'favorite_genre': user_data.get_favorite_genre(),
        'loan_history': loan_history,
        'read_books': read_books,
    }

    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{user.username}_data.json"'
    return response

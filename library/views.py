from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Book, Loan
from .forms import CustomUserCreationForm
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import UserData, Book
from django.db.models import Count
import json
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

class BookListView(ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"

@login_required
def account(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, "library/account.html", {"loans": loans})
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

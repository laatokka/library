from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Book, Loan
from .forms import CustomUserCreationForm

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

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Book, Loan

def index(request):
    return render(request, 'index.html')

@require_POST
@login_required
def loan_book(request):
    try:
        data = json.loads(request.body)
        nfc_tag = data.get('nfc_tag')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not nfc_tag:
        return JsonResponse({'error': 'nfc_tag is required'}, status=400)

    try:
        book = Book.objects.get(nfc_tag=nfc_tag)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    # Check if book is already loaned (return_date is null)
    if Loan.objects.filter(book=book, return_date__isnull=True).exists():
        return JsonResponse({'error': 'Book is already on loan'}, status=400)

    loan = Loan.objects.create(user=request.user, book=book)

    return JsonResponse({
        'message': 'Loan created successfully',
        'book': book.name,
        'loan_id': loan.id
    })

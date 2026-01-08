from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loan-book/', views.loan_book, name='loan_book'),
]

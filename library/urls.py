from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loan-book/', views.loan_book, name='loan_book'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.account, name='account'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('account/', views.account_view, name='account'),
    path('account/download/', views.download_user_data, name='download_user_data'),
    path('account/toggle-read/<int:book_id>/', views.toggle_book_read, name='toggle_book_read'),
]

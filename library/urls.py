from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account_view, name='account'),
    path('account/download/', views.download_user_data, name='download_user_data'),
    path('account/toggle-read/<int:book_id>/', views.toggle_book_read, name='toggle_book_read'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('all_books',views.get_all_books, name="get_all_books"),
    path('get_book/<int:book_id>',views.get_book),
    path('create_book', views.create_book),
    path('update_book', views.update_book),
    path('delete_book/<int:book_id>',views.delete_book),
    
]


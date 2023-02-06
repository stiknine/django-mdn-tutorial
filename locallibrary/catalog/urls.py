from django.urls import path
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),
    path('book/<uuid:bookinstance_id>/renew/', views.renew_book, name='renew'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name='author-delete'),
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedListView.as_view(), name='borrowed'),
]

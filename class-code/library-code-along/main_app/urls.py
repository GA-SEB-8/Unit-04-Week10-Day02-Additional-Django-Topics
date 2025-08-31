from django.urls import path
from . import views


urlpatterns = [

    # FBV:
    path("authors/", views.author_list, name="author_list"),
    # path("authors/new/", views.author_create, name="author_create"),
    path("authors/<int:pk>/", views.author_detail, name="author_detail"),
    # path("authors/<int:pk>/edit/", views.author_update, name="author_update"),
    # path("authors/<int:pk>/delete/", views.author_delete, name="author_delete"),


    # CBV:
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("authors/new/", views.AuthorCreateView.as_view(), name="author_create"),
    # path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("authors/<int:pk>/edit/", views.AuthorUpdateView.as_view(), name="author_update"),
    path("authors/<int:pk>/delete/", views.AuthorDeleteView.as_view(), name="author_delete"),

    # Book CBV:
    path("books/new/",views.BookCreateView.as_view(), name='book_create'),
    path("books/",views.BookListView.as_view(), name='book_list'),
    path("books/<int:book_id>/update/",views.BookUpdateView.as_view(), name='book_create'),
    path("books/<int:book_id>/",views.BookDetailView.as_view(), name='book_detail'),
    path("books/<int:pk>/delete/",views.BookDeleteView.as_view(), name='book_delete'),
    path("auth/signup",views.SignUpView.as_view(), name="signup")






# 1. create the view function or class
# 2. add the view in the urls.py
# 3. create the html file in the templates folder

]

from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "is_best_seller"]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','published_year','in_print','author']


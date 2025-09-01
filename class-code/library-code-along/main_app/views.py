from django.shortcuts import render, redirect
from .models import Author
from .forms import AuthorForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def author_list(request):
    authors = Author.objects.all()
    print(authors)
    return render(request, "authors/author_list.html", {"authors": authors})

def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    books = author.books.all()
    print(author.books.all())
    return render(request, "authors/author_detail.html", {"author": author, 'books':books})

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm()
    return render(request, "authors/author_form.html", {"form": form})

def author_update(request, pk):
    author = Author.objects.get(pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm(instance=author)
    return render(request, "authors/author_form.html", {"form": form})

def author_delete(request, pk):
    author = Author.objects.get(pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect("author_list")
    return render(request, "authors/author_confirm_delete.html", {"author": author})




# CBV:
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Author, Book
from .forms import AuthorForm, BookForm


class AuthorListView(ListView):
    model = Author
    template_name = "authors/author_list.html"
    context_object_name = "authors"


class AuthorDetailView(DetailView):
    model = Author
    template_name = "authors/author_detail.html"
    context_object_name = "author"


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['books'] = Book.objects.filter(author)

        return 


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "authors/author_form.html"


    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.pk})


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "authors/author_form.html"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.pk})


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "authors/author_confirm_delete.html"
    success_url = reverse_lazy("author_list")





# Books Views
class BookCreateView(LoginRequiredMixin,CreateView):
    model = Book
    template_name = 'books/book-form.html'
    form_class = BookForm
    # success_url = reverse_lazy("book_list")

    def get_success_url(self):
        return reverse('book_detail',kwargs={'book_id':self.object.pk})

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    template_name = 'books/book-form.html'
    form_class = BookForm
    success_url = "/books/"
    pk_url_kwarg = 'book_id' #change the dynamic url in the urls.py


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id' #change the dynamic url in the urls.py


# Gets the favorites for the user for this book if he did favorite it
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['did_favorite'] = BookFavorite.objects.filter(user = user, book = self.object).exists()
        return ctx


class BookDeleteView(DeleteView):
    model = Book
    success_url = "/books/"

    


from django.contrib.auth.decorators import login_required
# FBV Books:
def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, "books/book_detail.html", {"book": book})



@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect(reverse("book_detail", kwargs={"pk": book.pk}))
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form})






# Auth steps:
# 1: add the path in the urls.py of your project
# 2: add the redirects to your settings.py
# 3: in the base.html lets change the navbar if we are logged in


from django.contrib.auth.models import User # this is the user model we use to log in
from django.contrib.auth.forms import UserCreationForm
import requests
from .models import BookFavorite
class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/sign-up.html'
    


def call_api(request):
    res = requests.get("https://omar-ga-class.onrender.com/students")
    post_response = requests.post("https://omar-ga-class.onrender.com/students",{"name":"NEW STUDENT!!!!!!"})
    print(res.json()[0]['course'])

    BookFavorite.objects.filter(user=request.user)
    return render(request,'registration/sign-up.html')




# Adding a book to the favorites

class toggle_book_fav(LoginRequiredMixin,View):
    def post(self, request,pk):
        book = Book.objects.get(pk=pk)
        fav, created = BookFavorite.objects.get_or_create(user = request.user, book=book)
        if not created:
            fav.delete()
        return redirect('book_detail', book_id=book.pk)
    


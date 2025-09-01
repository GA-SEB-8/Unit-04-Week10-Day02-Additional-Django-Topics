from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.




class Author(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_best_seller = models.BooleanField(default=False)

    class Meta:
        db_table = "authors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=150)
    published_year = models.PositiveIntegerField(null=True)
    in_print = models.BooleanField(default=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    # Author.objects.books_written()

    cover_image = models.ImageField(upload_to='book_covers/', null=True)

    class Meta:
        db_table = 'books'
    
    def __str__(self):
        return self.title
    
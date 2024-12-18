from django.contrib import admin
from .models import Author, Book, BookCopy

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)

from django.contrib import admin
from .models import Author, Book, BookCopy, Cart

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Cart)

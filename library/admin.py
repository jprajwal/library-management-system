from django.contrib import admin
from .models import Author, Book, BookCopy, CartItem, BookRent, Transaction

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(CartItem)
admin.site.register(BookRent)
admin.site.register(Transaction)

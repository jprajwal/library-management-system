from .models import Book, Author, BookCopy, CartItem
from enum import Enum
from datetime import timedelta
from django.contrib.auth.models import User


class BooksSearchCriteria(Enum):
    AUTHOR = "AUTHOR"
    TITLE = "TITLE"


class BooksController:
    @staticmethod
    def browse() -> list[Book]:
        return list(Book.objects.all())

    @staticmethod
    def search(criteria: BooksSearchCriteria, query_str: str) -> list[Book]:
        if criteria == BooksSearchCriteria.AUTHOR:
            return list(Book.objects.filter(author__name__contains=query_str))
        elif criteria == BooksSearchCriteria.TITLE:
            return list(Book.objects.filter(title__contains=query_str))
        else:
            raise Exception("invalid search criteria")

    @staticmethod
    def add_book(**kwargs) -> None:
        author = Author.objects.get(pk=kwargs["author"])
        book = Book(
            title=kwargs["title"],
            rent_cost=int(kwargs["rent_cost"]),
            max_rent_period=timedelta(days=int(kwargs["max_rent_period"]))
        )
        book.save()
        book.author.set([author])


class BookCopiesController:
    @staticmethod
    def get(book_id: int) -> list[BookCopy]:
        copies = BookCopy.objects.filter(book_id=book_id)
        return list(copies)

    @staticmethod
    def get_copy(bookcopy_id: int) -> BookCopy:
        copy = BookCopy.objects.get(id=bookcopy_id)
        return copy

    @staticmethod
    def create_new_copies(book_id: int, count: int) -> None:
        copies = BookCopiesController.get(book_id=book_id)
        if copies:
            raise Exception("book already has copies")
        for _ in range(count):
            BookCopy.objects.create(book_id=Book.objects.get(id=book_id))

    @staticmethod
    def add_copies(book_id: int, count: int) -> None:
        copies = BookCopiesController.get(book_id=book_id)
        if not copies:
            raise Exception("book copies cannot be updated since they don't exist")
        for _ in range(count):
            BookCopy.objects.create(book_id=Book.objects.get(id=book_id))

    @staticmethod
    def delete_bookcopy(bookcopy_id: int) -> None:
        copy = BookCopy.objects.get(pk=bookcopy_id)
        copy.delete()


class CartItemsController:
    @staticmethod
    def get_cartitems(user: User) -> list[CartItem]:
        return list(CartItem.objects.filter(userid=user.id))

    @staticmethod
    def add_cartitem(user: User, bookcopy_id: int) -> None:
        # TODO: check if bookcopy_id is available in library
        copy = BookCopiesController.get_copy(bookcopy_id)
        # TODO: check if bookcopy_id is already added in user's cart.
        cart_item = CartItem(userid=user, book_copy=copy)
        cart_item.save()

    @staticmethod
    def delete_cartitem(user: User, cartitem_id: int) -> None:
        cart_item = CartItem.objects.get(id=cartitem_id)
        cart_item.delete()
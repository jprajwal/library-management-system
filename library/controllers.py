from datetime import timedelta
from enum import Enum
from typing import Any

from django.contrib.auth.models import User

from .models import Author, Book, BookCopy, CartItem
from .queriable import Data, DataGetter


class OrderedBookDataGetter(DataGetter[Book]):
    def __init__(self, order: str = "ascend") -> None:
        self.order = order

    def get_data(self, qs) -> Data[Book]:
        match self.order:
            case "ascend":
                return Data[Book](qs)
            case "descend":
                return Data[Book](qs.reverse())
            case _:
                raise Exception("Invalid order criteria provided.")


class FilteredBookDataGetter(DataGetter[Book]):
    def __init__(self, filter_info: dict[str, Any]):
        self.filter_info = filter_info

    def get_data(self, qs) -> Data[Book]:
        filters = {}
        for key, value in self.filter_info.items():
            filter_ = key
            match value["matchby"]:
                case "contains":
                    filter_ += "__contains"
                case _:
                    raise Exception("Unknown matchby criteria provided")
            filters[filter_] = value["value"]
        print(f"{filters=}")
        return Data[Book](qs.filter(**filters))


class BooksSearchCriteria(Enum):
    AUTHOR = "AUTHOR"
    TITLE = "TITLE"


class BooksController:
    def __init__(self):
        super().__init__()
        self._model = Book

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
            max_rent_period=timedelta(days=int(kwargs["max_rent_period"])),
        )
        book.save()
        book.author.set([author])

    @staticmethod
    def get_all() -> Data[Book]:
        return Data[Book](Book.objects.all())


class BookCopiesController:
    def __init__(self):
        super().__init__()
        self._model = BookCopy

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
    def __init__(self):
        super().__init__()
        self._model = CartItem

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

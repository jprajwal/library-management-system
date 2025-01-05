from typing import Any, Iterable

from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Author, Book, BookCopy, CartItem
from .queriable import DataGetter, PaginatedDjangoModelDataGetter


class AllBookDataGetter(DataGetter[Book]):
    def get_data(self) -> Iterable[Book]:
        return Book.objects.all()


class OrderedBookDataGetter(DataGetter[Book]):
    def __init__(self, order: str) -> None:
        self.order = order

    def get_data(self) -> Iterable[Book]:
        match self.order:
            case "ascending":
                return Book.objects.all()
            case "desending":
                return Book.objects.all().reverse()
            case _:
                raise Exception("Unsupported order criteria provided")


class FilteredBookDataGetter(DataGetter[Book]):
    def __init__(self, filter_info: dict[str, Any] = None) -> None:
        self.data = Book.objects.all()
        # protocol for defining filter data:
        # filter data must be defined as a dictionary called filter-dict.
        # The filter-dict's keys are the db fields by which the data must
        # filtered.
        # The filter-dict's values are also a dictionary called filter-value.
        # The filter-value dict is must comprise of 2 mandatory keys.
        # The first key is: "value" and the associated value is the the filter
        # which is the data by which the db data must be filtered.
        # The second key is: "matchby" and the associated value is a string
        # specifies how the "value" must be matched against the db data.
        # For example, {"name": {"matchby": "contains", "value": "johndoe"}}
        # filters the db data if the name field of the records contains "johndoe"
        # in them.
        self.filter_info: dict[str, Any] = filter_info or {}

    def get_data(self) -> Iterable[Book]:
        filters = {}
        for key, value in self.filter_info.items():
            filter_ = key
            match value["matchby"]:
                case "contains":
                    filter_ += "__contains"
                case _:
                    raise Exception("Unknown matchby criteria provided")
            filters[key] = filter_
        data = self.data.filter(**filters)
        return data


class PaginatedBookDataGetter(PaginatedDjangoModelDataGetter):
    def __init__(self, data: DataGetter[Book], page: int, perpage: int) -> None:
        super().__init__(data, page, perpage)


class BookCopiesController(PaginatedDjangoModelDataGetter):
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


class CartItemsController(PaginatedDjangoModelDataGetter):
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

from typing import Any, Iterator, TypeVar, Generic

from collections.abc import Iterable as ABCIterable
from django.contrib.auth.models import User
from django.db.models import QuerySet, Model
from .models import Book, BookCopy, CartItem

T = TypeVar('T')
DjangoModel = TypeVar('DjangoModel', bound=Model, covariant=True)


class Result(Generic[DjangoModel], ABCIterable):
    def __init__(self, query: QuerySet) -> None:
        self.query = query
        self.iter = None

    def filter(self, filter_info: dict[str, Any]) -> 'Result[DjangoModel]':
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
        filters = {}
        for key, value in filter_info.items():
            filter_ = key
            match value["matchby"]:
                case "contains":
                    filter_ += "__contains"
                case _:
                    raise Exception("Unknown matchby criteria provided")
            filters[key] = filter_
        return Result(self.query.filter(**filters))

    def order(self, order_type: str) -> 'Result[DjangoModel]':
        match order_type:
            case "ascending":
                return Result(self.query.all())
            case "desending":
                return Result(self.query.all().reverse())
            case _:
                raise Exception("Unsupported order criteria provided")

    def __iter__(self) -> Iterator[DjangoModel]:
        self.iter = iter(self.query)
        return self

    def __next__(self) -> DjangoModel:
        if self.iter is None:
            self.iter = iter(self.query)
        return next(self.iter)


class BookController:
    @staticmethod
    def books() -> Result[Book]:
        return Result(Book.objects.all())


class BookCopyController:
    @staticmethod
    def get(bookcopy_id: int) -> Result[BookCopy]:
        copies = BookCopy.objects.get(id=bookcopy_id)
        return Result(copies)

    @staticmethod
    def get_copies_by_book_id(book_id: int) -> Result[BookCopy]:
        copy = BookCopy.objects.filter(book_id=book_id)
        return Result(copy)

    @staticmethod
    def add_copies(book_id: int, count: int) -> None:
        for _ in range(count):
            BookCopy.objects.create(book_id=Book.objects.get(id=book_id))

    @staticmethod
    def delete_copy(bookcopy_id: int) -> None:
        copy = BookCopy.objects.get(pk=bookcopy_id)
        copy.delete()


class CartItemController:
    @staticmethod
    def cart_items(user: User) -> Result[CartItem]:
        return Result(CartItem.objects.filter(userid=user.id))

    @staticmethod
    def add_cart_item(user: User, bookcopy_id: int) -> None:
        # TODO: check if bookcopy_id is available in library
        copy = BookCopyController.get(bookcopy_id)
        # TODO: check if bookcopy_id is already added in user's cart.
        cart_item = CartItem(userid=user, book_copy=copy)
        cart_item.save()

    @staticmethod
    def delete_cart_item(user: User, cart_item_id: int) -> None:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

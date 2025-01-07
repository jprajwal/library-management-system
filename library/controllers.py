from typing import Any, Generic, TypeVar

from django.contrib.auth.models import User
from django.db.models import Model

from .interfaces import Data, DataGetter
from .models import Book, BookCopy, CartItem

DjangoModel = TypeVar("DjangoModel", bound=Model, covariant=True)


class OrderedDataGetter(Generic[DjangoModel], DataGetter[DjangoModel]):
    def __init__(self, order: str = "ascend") -> None:
        self.order = order

    def get_data(self, qs) -> Data[DjangoModel]:
        match self.order:
            case "ascend":
                return Data[DjangoModel](qs)
            case "descend":
                return Data[DjangoModel](qs.reverse())
            case _:
                raise Exception("Invalid order criteria provided.")


class FilteredDataGetter(Generic[DjangoModel], DataGetter[DjangoModel]):
    def __init__(self, filter_info: dict[str, Any]):
        self.filter_info = filter_info

    def get_data(self, qs) -> Data[DjangoModel]:
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
        return Data[DjangoModel](qs.filter(**filters))


class AllBookDataGetter(DataGetter[Book]):
    def get_data(self, _):
        return Data[Book](Book.objects.all())


class AllBookCopyDataGetter(DataGetter[BookCopy]):
    def get_data(self, _):
        return Data[BookCopy](BookCopy.objects.all())


class AllBookCopyDataGetter(DataGetter[CartItem]):
    def get_data(self, _):
        return Data[CartItem](CartItem.objects.all())


OrderedBookDataGetter = OrderedDataGetter[Book]
OrderedBookCopyDataGetter = OrderedDataGetter[BookCopy]
OrderedCartItemDataGetter = OrderedDataGetter[CartItem]


class FilteredBookDataGetter(FilteredDataGetter[Book]):
    def get_data(self, qs) -> Data[Book]:
        if "author" in self.filter_info:
            author_info = self.filter_info.pop("author")
            self.filter_info["author__name"] = author_info
        return super().get_data(qs)


FilteredBookCopyDataGetter = FilteredDataGetter[BookCopy]
FilteredCartItemDataGetter = FilteredDataGetter[CartItem]


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

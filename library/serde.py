from .models import Book, CartItem, CartItemType
from json import JSONEncoder
from typing import Any


def serialize_book(book: Book) -> dict[str, Any]:
    d = {
        "id": book.id,
        "title": book.title,
        "authors": ",".join(book.author.values_list("name", flat=True)),
        # "rent_cost": book.rent_cost,
        # "max_rent_period": book.max_rent_period,
    }
    return d


def serialize_cartitem(cart_item: CartItem) -> dict[str, Any]:
    d = {
        "id": cart_item.id,
        "item_type": cart_item.item_type,
        "item_info": {},
        "requested_count": cart_item.requested_count,
    }
    if cart_item.item_type == CartItemType.BOOK:
        book = Book.objects.get(pk=cart_item.product_id)
        d["item_info"].update(serialize_book(book))
    return d


class BookEncoder(JSONEncoder):
    def default(self, o):
        if not isinstance(o, Book):
            return super().default(o)
        return serialize_book(o)


class CartItemEncoder(JSONEncoder):
    def default(self, o: CartItem | Any):
        if not isinstance(o, CartItem):
            return super().default(o)
        return serialize_cartitem(o)

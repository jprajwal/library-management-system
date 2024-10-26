from .models import Book, Author
from enum import Enum
from datetime import timedelta


class BookCatalogSearchCriteria(Enum):
    AUTHOR = "AUTHOR"
    TITLE = "TITLE"


class BookCatalog:
    @staticmethod
    def browse() -> list[Book]:
        return list(Book.objects.all())

    @staticmethod
    def search(criteria: BookCatalogSearchCriteria, query_str: str) -> list[Book]:
        if criteria == BookCatalogSearchCriteria.AUTHOR:
            return list(Book.objects.filter(author__name__contains=query_str))
        elif criteria == BookCatalogSearchCriteria.TITLE:
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

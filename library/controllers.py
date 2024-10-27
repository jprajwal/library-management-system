from .models import Book, Author, BookCopy
from enum import Enum
from datetime import timedelta


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
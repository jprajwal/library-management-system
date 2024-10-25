from .models import Book


class BookCatalog:
    @staticmethod
    def browse() -> list[Book]:
        return list(Book.objects.all())

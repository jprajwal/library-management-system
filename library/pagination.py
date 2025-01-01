from typing import Generic, TypeVar


T = TypeVar('T')


class PaginatedData(Generic[T]):
    def __init__(
        self,
        items: list[T] | None = None,
        prev: bool = False,
        next: bool = False
    ) -> None:
        self.items = items
        self.prev = prev
        self.next = next


class Pagination(Generic[T]):
    def __init__(self, items: list[T]) -> None:
        self.items = items

    def paginate(self, page: int, perpage: int) -> PaginatedData[T]:
        ...

from typing import Generic, TypeVar, Iterable
from .queriable import PaginationQueriable


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
    def __init__(self, queriable: PaginationQueriable[T]) -> None:
        self._queriable = queriable

    def paginate(self, page: int, perpage: int) -> PaginatedData[T]:
        start = (page - 1) * perpage
        end = page * perpage
        ls = self._queriable.get_data_by_range(start, end)
        return PaginatedData(
            ls,
            prev=self._queriable.has_before(start),
            next=self._queriable.has_beyond(end-1)
        )

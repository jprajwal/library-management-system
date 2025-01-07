from typing import Generic, Iterator, TypeVar

from .interfaces import Data

T = TypeVar("T", covariant=True)


class PaginatedData(Generic[T]):
    def __init__(
        self,
        items: Iterator[T] | None = None,
        has_prev: bool = False,
        has_next: bool = False,
    ) -> None:
        self.items = items
        self.has_prev = has_prev
        self.has_next = has_next


class Pagination(Generic[T]):
    def __init__(self, data: Data[T]) -> None:
        self._data = data

    def paginate(self, page: int, perpage: int) -> PaginatedData[T]:
        start = (page - 1) * perpage
        end = page * perpage
        objs = self._data.iterator()
        has_prev = False
        has_next = False
        for _ in range(start):
            try:
                next(objs)
                has_prev = True
            except StopIteration:
                return PaginatedData(iter([]), has_prev=has_prev, has_next=has_next)
        ls = []
        for _ in range(start, end + 1):
            try:
                ls.append(next(objs))
            except StopIteration:
                return PaginatedData(iter(ls), has_prev=has_prev, has_next=has_next)
        if len(ls) > (end - start):
            has_next = True
            ls = ls[:-1]
        return PaginatedData(iter(ls), has_prev=has_prev, has_next=has_next)

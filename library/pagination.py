from typing import Generic, TypeVar, Iterable


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
    def __init__(self, page: int = 1, perpage: int = 50) -> None:
        self.page = page
        self.perpage = perpage

    def paginate(self, iterable: Iterable) -> PaginatedData[T]:
        page, perpage = self.page, self.perpage
        assert page > 0 and perpage > 0
        start = (page - 1) * perpage
        end = page * perpage
        ls = []
        has_beyond = False
        has_before = False
        for i, item in enumerate(iterable):
            if i > 0:
                has_before = True
            if i < start:
                continue
            if i == end:
                has_beyond = True
                break
            ls.append(item)

        return PaginatedData(
            ls,
            prev=has_before,
            next=has_beyond,
        )

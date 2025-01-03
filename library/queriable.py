from typing import Generic, TypeVar, Protocol
from django.db.models import Model


T = TypeVar('T')
DjangoModel = TypeVar('DjangoModel', bound=Model, covariant=True)


class PaginationQueriable(Protocol, Generic[T]):
    def get_data_by_range(self, start: int, end: int) -> list[T]:
        ...

    def has_beyond(self, index: int) -> bool:
        ...

    def has_before(self, index: int) -> bool:
        ...


class DefaultPaginationQueriableImplForDjango(
    PaginationQueriable, Generic[DjangoModel]
):
    def __init__(self) -> None:
        self._model: DjangoModel | None = None

    def get_data_by_range(self, start: int, end: int) -> list[DjangoModel]:
        assert self._model is not None
        objs = self._model.objects.all().iterator()
        to_return = []
        for _ in range(start):
            try:
                next(objs)
            except StopIteration:
                return []
        for _ in range(start, end):
            try:
                to_return.append(next(objs))
            except StopIteration:
                break
        return to_return

    def has_beyond(self, index: int) -> bool:
        assert self._model is not None
        count = self._model.objects.count()
        return count > index + 1

    def has_before(self, index: int) -> bool:
        assert self._model is not None
        count = self._model.objects.count()
        if index <= 0:
            return False
        return count > 0

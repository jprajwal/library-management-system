from typing import Generic, TypeVar, Protocol, Iterable
from django.db.models import Model


T = TypeVar('T', covariant=True)
DjangoModel = TypeVar('DjangoModel', bound=Model, covariant=True)


class DataGetter(Protocol, Generic[T]):
    def get_data(self) -> Iterable[T]:
        raise NotImplementedError()


class PaginationQueriable(Protocol, Generic[T]):
    def has_beyond(self) -> bool:
        raise NotImplementedError()

    def has_before(self) -> bool:
        raise NotImplementedError()


class PaginationDataGetter(Generic[T], DataGetter[T], PaginationQueriable[T]):
    ...


class PaginatedDjangoModelDataGetter(
    Generic[DjangoModel], PaginationDataGetter[DjangoModel]
):
    def __init__(self, data: DataGetter[DjangoModel], page: int, perpage: int) -> None:
        self.data = data
        self.page = page
        self.perpage = perpage
        self._computed_data: Iterable[DjangoModel] | None = None
        self._has_beyond: bool | None = None
        self._has_before: bool | None = None

    def get_data(self) -> Iterable[DjangoModel]:
        if self._computed_data is not None:
            return self._computed_data
        objs = self.data.get_data().__iter__()
        to_return = []
        start = (self.page - 1) * self.perpage
        end = (self.page * self.perpage)
        if start == 0:
            self._has_before = False
        for _ in range(start):
            try:
                next(objs)
                if self._has_before is None:
                    self._has_before = True
            except StopIteration:
                self._computed_data = []
                return self._computed_data
        for _ in range(start, end+1):
            try:
                to_return.append(next(objs))
            except StopIteration:
                self._has_beyond = False
                break
        if len(to_return) > (end - start):
            self._has_beyond = True
            to_return = to_return[:-1]
        self._computed_data = to_return
        return self._computed_data

    def has_beyond(self) -> bool:
        if self._has_beyond is None:
            raise Exception(
                "this value is not yet computed. Call get_data() before getting this info"
            )
        return self._has_beyond

    def has_before(self) -> bool:
        if self._has_before is None:
            raise Exception(
                "this value is not yet computed. Call get_data() before getting this info"
            )
        return self._has_before

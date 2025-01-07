from typing import Callable, Generic, Iterator, Protocol, TypeVar

from django.db.models import Model, QuerySet

T = TypeVar("T", covariant=True)
DjangoModel = TypeVar("DjangoModel", bound=Model, covariant=True)


class Data(Generic[T]):
    def __init__(self, qs: QuerySet) -> None:
        self.qs = qs

    # def apply(self, f: Callable[[QuerySet], "Data[T]"]) -> "Data[T]":
    def transform(self, dg: "DataGetter[T]") -> "Data[T]":
        return dg.get_data(self.qs)

    def transform_if(
        self, predicate: Callable[[], bool], dg: "DataGetter[T]"
    ) -> "Data[T]":
        if predicate():
            return dg.get_data(self.qs)
        return self

    def iterator(self) -> Iterator[T]:
        return self.qs.iterator()


class DataGetter(Generic[T], Protocol):
    def get_data(self, qs: QuerySet) -> Data[T]: ...

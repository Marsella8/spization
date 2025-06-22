from itertools import chain
from typing import Callable, Iterable


def get_only[T](container: Iterable[T]) -> T:
    c = list(container)
    if len(c) != 1:
        raise ValueError(f"Container must only have 1 item, has {len(c)}")
    return c[0]


def get_any[T](container: Iterable[T]) -> T:
    return next(iter(container))


def flatmap[T, U](
    func: Callable[[T], Iterable[U]], iterable: Iterable[T]
) -> Iterable[U]:
    return chain.from_iterable(map(func, iterable))


__all__ = ["get_any", "get_only", "flatmap"]

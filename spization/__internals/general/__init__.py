from functools import reduce
from itertools import chain
from typing import Callable, Iterable


def get_only[T](container: Iterable[T]) -> T:
    c = list(container)
    if len(c) != 1:
        raise ValueError(f"Container must only have 1 item, has {len(c)}")
    return c[0]


def get_any[T](container: Iterable[T]) -> T:
    return next(iter(container))


def must[T](value: T | None) -> T:
    if value is None:
        raise ValueError("Used must() on a None value.")
    return value


def flatmap[T, U](
    func: Callable[[T], Iterable[U]], iterable: Iterable[T]
) -> Iterable[U]:
    return chain.from_iterable(map(func, iterable))


def are_all_equal[T](iterable: Iterable[T]) -> bool:
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def are_all_disjoint[T](iterable: Iterable[set[T] | frozenset[T]]) -> bool:
    sets = list(iterable)
    if not sets:
        return True
    union = reduce(lambda x, y: x.union(y), sets)
    return len(union) == sum(len(s) for s in sets)


__all__ = [
    "get_any",
    "get_only",
    "must",
    "flatmap",
    "are_all_equal",
    "are_all_disjoint",
]

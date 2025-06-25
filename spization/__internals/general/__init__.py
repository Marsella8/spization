from itertools import chain
from functools import reduce
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

def are_all_equal[T](iterable: Iterable[T]) -> bool:
    if len(iterable) == 0:
        return True
    first = next(iter(iterable))
    return all(first == x for x in iterable)

def are_all_disjoint[T](iterable: Iterable[set[T] | frozenset[T]]) -> bool:
    union = reduce(lambda x, y: x.union(y), iterable)
    return len(union) == sum(len(s) for s in iterable)


__all__ = ["get_any", "get_only", "flatmap", "are_all_equal", "are_all_disjoint"]

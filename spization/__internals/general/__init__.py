from typing import Any, Iterable


def get_only(container: Iterable[Any]) -> Any:
    c = list(container)
    if len(c) != 1:
        raise ValueError("Container must only have 1 item")
    return c[0]


def get_any(container: Iterable[Any]) -> Any:
    return next(iter(container))


__all__ = ["get_any", "get_only"]

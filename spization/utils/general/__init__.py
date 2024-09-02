from typing import Any, Iterable


def get_only(container: Iterable[Any]) -> Any:
    if len(list(container)) != 1:
        raise ValueError("Container must only have 1 item")
    return next(iter(container))


def get_any(container: Iterable[Any]) -> Any:
    return next(iter(container))


__all__ = ["get_any", "get_only"]

from typing import Any, Iterable

def get_only(container : Iterable[Any]):
    if len(list(container)) != 1:
        raise ValueError
    return next(iter(container))


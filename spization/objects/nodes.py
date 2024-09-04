from dataclasses import dataclass, field
from typing import Any

PureNode = int


@dataclass(slots=True, frozen=True)
class DupNode:
    node: int
    dup_id: int


Node = PureNode | DupNode


class SyncNode:
    id: int = field(init=False)
    _counter: int = 0

    def __init__(self) -> None:
        SyncNode._counter += 1
        self.id = SyncNode._counter


class DummyNode:
    id: Any = field(init=False)
    _counter: int = 0

    def __init__(self) -> None:
        DummyNode._counter += 1
        self.id = DummyNode._counter

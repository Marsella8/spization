from dataclasses import dataclass, field
from typing import Any

PureNode = int


@dataclass(slots=True, frozen=True)
class DupNode:
    node: int
    dup_id: int


# TODO define a better node hierarchy
# Node is all nodes.
# TODO add __Eq__ and things like that


class SyncNode:
    id: int = field(init=False)
    _counter: int = 0

    def __init__(self) -> None:
        SyncNode._counter += 1
        self.id = SyncNode._counter

    def __repr__(self) -> str:
        return f"SyncNode({self.id})"


class DummyNode:
    id: Any = field(init=False)
    _counter: int = 0

    def __init__(self) -> None:
        DummyNode._counter += 1
        self.id = DummyNode._counter

    def __repr__(self) -> str:
        return f"DummyNode({self.id})"


Node = PureNode | DupNode | DummyNode | SyncNode

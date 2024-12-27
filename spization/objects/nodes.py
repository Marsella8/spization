from dataclasses import field
from typing import Any

PureNode = int


class SyncNode:
    id: int = field(init=False)
    _counter: int = 0

    def __init__(self, val: int | None = None) -> None:
        if val is None:
            SyncNode._counter += 1
            self.id = SyncNode._counter
        else:
            self.id = val

    def __repr__(self) -> str:
        return f"SyncNode({self.id})"

    def __eq__(self, other):
        if not isinstance(other, SyncNode):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class DummyNode:
    id: Any = field(init=False)
    _counter: int = 0

    def __init__(self) -> None:
        DummyNode._counter += 1
        self.id = DummyNode._counter

    def __repr__(self) -> str:
        return f"DummyNode({self.id})"


Node = PureNode | DummyNode | SyncNode

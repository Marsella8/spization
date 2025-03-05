from dataclasses import field
from enum import Enum, auto
from typing import Union

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SyncNode):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


Node = Union[PureNode, SyncNode]


class NodeRole(Enum):
    STANDARD = auto()
    DUMMY = auto()
    SYNC = auto()


# TODO: all nodes are now ints, if you want to distinguish you now need to have a node_type map

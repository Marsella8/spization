from enum import Enum, auto
from typing import Iterable, TypeAlias

Node: TypeAlias = int


class NodeRole(Enum):
    PURE = auto()
    DUMMY = auto()
    SYNC = auto()

def get_initial_node_role_map(nodes: Iterable[Node]) -> dict[Node, NodeRole]:
    return {node: NodeRole.PURE for node in nodes}

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Union

from spization.__internals.general import flatmap
from spization.objects.nodes import Node


@dataclass
class MDSeries:
    children: tuple[MDParallel | MDPrime | Node] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.children = tuple(self.children)

    def __hash__(self) -> int:
        return hash(self.children)

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        return f"S{tuple(self.children)}"

    @property
    def nodes(self) -> frozenset[Node]:
        return frozenset(
            flatmap(
                lambda child: {child} if isinstance(child, Node) else child.nodes,
                self.children,
            )
        )

    __str__ = __repr__


@dataclass
class MDParallel:
    children: frozenset[Union[MDSeries, "MDPrime", Node]] = field(
        default_factory=frozenset
    )

    def __post_init__(self) -> None:
        self.children = frozenset(self.children)

    def __hash__(self) -> int:
        return hash(self.children)

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        return f"P{tuple(self.children)}"

    @property
    def nodes(self) -> frozenset[Node]:
        return frozenset(
            flatmap(
                lambda child: {child} if isinstance(child, Node) else child.nodes,
                self.children,
            )
        )

    __str__ = __repr__


@dataclass
class MDPrime:
    children: frozenset[Union[MDSeries, MDParallel, Node]] = field(
        default_factory=frozenset
    )

    def __post_init__(self) -> None:
        self.children = frozenset(self.children)

    def __hash__(self) -> int:
        return hash(self.children)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterable[MDSeries | MDParallel | Node]:
        return iter(self.children)

    def __repr__(self) -> str:
        return f"Z{tuple(self.children)}"

    @property
    def nodes(self) -> frozenset[Node]:
        return frozenset(
            flatmap(
                lambda child: {child} if isinstance(child, Node) else child.nodes,
                self.children,
            )
        )

    __str__ = __repr__


ModularDecompositionTree = Node | MDParallel | MDSeries | MDPrime

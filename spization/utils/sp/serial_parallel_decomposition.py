from typing import Union, Iterator
from collections import Counter
from dataclasses import dataclass
from multimethod import multimethod


Node = int


@dataclass(slots=True)
class Parallel:
    children: Counter[Union["Serial", Node]]

    def __post_init__(self) -> None:
        self.children = Counter(self.children)

    def __hash__(self) -> Node:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"P{tuple(self.children.elements())}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Serial", Node]]:
        return iter(self.children.elements())

    def __len__(self) -> Node:
        return len(self.children)


@dataclass(slots=True)
class Serial:
    children: list[Union["Parallel", Node]]

    def __post_init__(self) -> None:
        self.children = list(self.children)

    def __hash__(self) -> Node:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"S{tuple(self.children)}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Parallel", Node]]:
        return iter(self.children)

    def __len__(self) -> Node:
        return len(self.children)

    @multimethod
    def __getitem__(self, index: Node) -> Union["Parallel", Node]:
        return self.children[index]

    @multimethod
    def __getitem__(self, range: slice) -> "Serial":
        return Serial(self.children[range])


SerialParallelDecomposition = Union[Serial, Parallel, Node]


@dataclass(slots=True, unsafe_hash=True)
class DummyNode:
    id: int

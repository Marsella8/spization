from dataclasses import dataclass
from typing import Collection, Iterator, Sequence, Union

from multimethod import multimethod
from multiset import FrozenMultiset

from .nodes import Node


@dataclass(slots=True)
class Parallel:
    children: Collection[Union["Serial", Node]] = FrozenMultiset()

    def __post_init__(self) -> None:
        self.children = FrozenMultiset(self.children)

    def __hash__(self) -> int:
        return sum((hash(child) for child in self.children))

    def __str__(self) -> str:
        return f"P{tuple(self.children)}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Serial", Node]]:
        return iter(self.children)

    def __len__(self) -> Node:
        return len(self.children)


@dataclass(slots=True)
class Serial:
    children: Sequence[Union["Parallel", Node]] = ()

    def __post_init__(self) -> None:
        self.children = tuple(self.children)

    def __hash__(self) -> int:
        return hash(self.children)

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


def S(*children: Union[Parallel, Node]) -> Serial:
    return Serial(children)


def P(*children: Union[Serial, Node]) -> Parallel:
    return Parallel(children)


# TODO: have nice formatting for long SP strings

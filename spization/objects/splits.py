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


@dataclass(slots=True)
class BinParallel:
    t1: "BinSerialParallelDecomposition"
    t2: "BinSerialParallelDecomposition"

    def __post_init__(self) -> None:
        # for term commutativity
        if self.t1 > self.t2:
            self.t1, self.t2 = self.t2, self.t1

    def __str__(self) -> str:
        return f"BP({self.t1}, {self.t2})"

    def __repr__(self) -> str:
        return self.__str__()

    def __gt__(self, other):
        if isinstance(other, Node):
            return True
        if isinstance(other, BinSerial):
            return True
        if isinstance(other, BinParallel):
            return (self.t1, self.t2) > (other.t1, other.t2)
        raise ValueError(
            f"BinParallel is not comparable with object of type {type(other)}"
        )

    def __lt__(self, other):
        return not (self > other)

    def __hash__(self):
        return hash((self.t1, self.t2))


@dataclass(slots=True)
class BinSerial:
    t1: "BinSerialParallelDecomposition"
    t2: "BinSerialParallelDecomposition"

    def __gt__(self, other):
        if isinstance(other, Node):
            return True
        if isinstance(other, BinParallel):
            return True
        if isinstance(other, BinSerial):
            return (self.t1, self.t2) > (other.t1, other.t2)
        raise ValueError(
            f"BinSerial is not comparable with object of type {type(other)}"
        )

    def __lt__(self, other):
        return not (self > other)

    def __str__(self) -> str:
        return f"BP({self.t1}, {self.t2})"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((self.t1, self.t2))


BinSerialParallelDecomposition = Union[BinSerial, BinParallel, Node]

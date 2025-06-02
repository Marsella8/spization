from dataclasses import dataclass
from typing import Collection, Iterator, Sequence, Union

from multimethod import multimethod
from multiset import FrozenMultiset

from .nodes import PureNode


@dataclass(slots=True)
class Parallel:
    children: Collection[Union["Serial", PureNode]] = FrozenMultiset()

    def __post_init__(self) -> None:
        self.children = FrozenMultiset(self.children)

    def __hash__(self) -> int:
        return sum((hash(child) for child in self.children))

    def __str__(self) -> str:
        return f"P{tuple(self.children)}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Serial", PureNode]]:
        return iter(self.children)

    def __len__(self) -> int:
        return len(self.children)


@dataclass(slots=True)
class Serial:
    children: Sequence[Union["Parallel", PureNode]] = ()

    def __post_init__(self) -> None:
        self.children = tuple(self.children)

    def __hash__(self) -> int:
        return hash(self.children)

    def __str__(self) -> str:
        return f"S{self.children}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Parallel", PureNode]]:
        return iter(self.children)

    def __len__(self) -> int:
        return len(self.children)

    @multimethod
    def __getitem__(self, index: PureNode) -> Union["Parallel", PureNode]:
        return self.children[index]

    @multimethod
    def __getitem__(self, range: slice) -> "Serial":
        return Serial(self.children[range])


SerialParallelDecomposition = Union[Serial, Parallel, PureNode]


def S(*children: Union[Parallel, PureNode]) -> Serial:
    return Serial(children)


def P(*children: Union[Serial, PureNode]) -> Parallel:
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

    def __gt__(self, other: object) -> bool:
        if isinstance(other, PureNode):
            return True
        if isinstance(other, BinSerial):
            return True
        if isinstance(other, BinParallel):
            return (self.t1, self.t2) > (other.t1, other.t2)
        raise ValueError(
            f"BinParallel is not comparable with object of type {type(other)}"
        )

    def __lt__(self, other: object) -> bool:
        return not (self > other)

    def __hash__(self) -> int:
        return hash((self.t1, self.t2))


@dataclass(slots=True)
class BinSerial:
    t1: "BinSerialParallelDecomposition"
    t2: "BinSerialParallelDecomposition"

    def __gt__(self, other: object) -> bool:
        if isinstance(other, PureNode):
            return True
        if isinstance(other, BinParallel):
            return True
        if isinstance(other, BinSerial):
            return (self.t1, self.t2) > (other.t1, other.t2)
        raise ValueError(
            f"BinSerial is not comparable with object of type {type(other)}"
        )

    def __lt__(self, other: object) -> bool:
        return not (self > other)

    def __str__(self) -> str:
        return f"BS({self.t1}, {self.t2})"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.t1, self.t2))


BinSerialParallelDecomposition = Union[BinSerial, BinParallel, PureNode]

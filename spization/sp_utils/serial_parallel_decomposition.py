from typing import Union, Iterator
from collections import Counter
from dataclasses import dataclass
from multimethod import multimethod


@dataclass
class Parallel:
    children: Counter[Union["Serial", int]]

    def __post_init__(self) -> None:
        self.children = Counter(self.children)

    def __hash__(self) -> int:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"P{tuple(self.children.elements())}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Serial", int]]:
        return iter(self.children.elements())

    def __len__(self) -> int:
        return len(self.children)


@dataclass
class Serial:
    children: list[Union["Parallel", int]]

    def __post_init__(self) -> None:
        self.children = list(self.children)

    def __hash__(self) -> int:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"S{tuple(self.children)}"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Union["Parallel", int]]:
        return iter(self.children)

    def __len__(self) -> int:
        return len(self.children)

    @multimethod
    def __getitem__(self, index: int) -> Union["Parallel", int]:
        return self.children[index]

    @multimethod
    def __getitem__(self, range: slice) -> "Serial":
        return Serial(self.children[range])


SerialParallelDecomposition = Union[Serial, Parallel, int]

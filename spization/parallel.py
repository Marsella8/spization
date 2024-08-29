from typing import Union
from collections import Counter
from dataclasses import dataclass
from serial import Serial

@dataclass
class Parallel:
    children: Counter[Union['Serial', int]]

    def __hash__(self) -> int:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"P({self.children}>"

    def __repr__(self) -> str:
        return self.__str__()

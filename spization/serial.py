from typing import Union
from dataclasses import dataclass

@dataclass
class Serial:
    children: list[Union['Parallel', int]]

    def __hash__(self) -> int:
        return hash(tuple(self.children))

    def __str__(self) -> str:
        return f"S({self.children}>"

    def __repr__(self) -> str:
        return self.__str__()

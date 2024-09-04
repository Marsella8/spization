from dataclasses import dataclass
from math import log
from random import choice, gauss, random
from typing import Callable

from spization.objects import Node


@dataclass(slots=True, frozen=True)
class Constant:
    value: float

    def __call__(self) -> float:
        return self.value


@dataclass(slots=True, frozen=True)
class Uniform:
    start: float
    stop: float

    def __post_init__(self) -> None:
        if self.start > self.stop:
            raise ValueError("start must be <= stop")

    def __call__(self) -> float:
        return self.start + (self.stop - self.start) * random()


@dataclass(slots=True, frozen=True)
class SampleFrom:
    values: set[float]

    def __call__(self) -> float:
        return choice(list(self.values))


@dataclass(slots=True, frozen=True)
class Exponential:
    param: float

    def __call__(self) -> float:
        return -1 / self.param * log(random())


@dataclass(slots=True, frozen=True)
class Gaussian:
    mean: float
    std: float

    def __call__(self) -> float:
        return gauss(self.mean, self.std)


def make_cost_map(nodes: set[Node], callable: Callable[[], float]) -> dict[Node, float]:
    cost_map = {node: callable() for node in nodes}
    assert all(
        val >= 0 for val in cost_map.values()
    ), "cost map should only sample from a non-negative distribution"
    return cost_map


def apply_noise(
    cost_map: dict[Node, float], noise: Callable[[], float]
) -> dict[Node, float]:
    noisy_cost_map = {node: cost * noise() for node, cost in cost_map.items()}
    assert all(
        val >= 0 for val in noisy_cost_map.values()
    ), "costs should be non-negative after noise"
    return noisy_cost_map

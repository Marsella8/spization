from networkx import DiGraph


def make_random_dag(num_nodes: int, p: float) -> DiGraph: ...


def make_random_local_dag(num_nodes: int, p: float, locality_ratio: float) -> DiGraph:
    """Like make_random_dag, but connections are limited to a local portion of the dag"""
    ...

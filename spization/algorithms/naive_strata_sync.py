from collections import defaultdict
from spization.utils import (
    sp_serial_composition,
    sp_parallel_composition,
)
from networkx import DiGraph
from spization import (
    SerialParallelDecomposition,
    Node,
)

from spization.utils.graph.properties import is_2_terminal_dag, is_compatible_graph
from spization.utils.graph.longest_path_lengths_from_source import (
    longest_path_lengths_from_source,
)
from spization.utils import normalize


def naive_strata_sync(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)

    longest_path_lengths: dict[Node, int] = longest_path_lengths_from_source(g)

    groups = defaultdict(list)
    for node, length in longest_path_lengths.items():
        groups[length].append(node)

    sp: SerialParallelDecomposition = sp_serial_composition(
        [
            sp_parallel_composition(list(group))
            for _, group in sorted(groups.items(), key=lambda t: t[0])
        ]
    )
    sp = normalize(sp)
    return sp

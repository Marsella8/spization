from collections import defaultdict
from spization.sp_utils.compositions import (
    sp_serial_composition,
    sp_parallel_composition,
)
from networkx import DiGraph
from spization.sp_utils.serial_parallel_decomposition import SerialParallelDecomposition
from spization.utils.graph import (
    single_source_longest_dag_path_length,
    is_2_terminal_dag,
    is_integer_graph,
    sources,
)
from spization.utils.utils import get_only
from spization.sp_utils.normalize import normalize


def naive_strata_sync(G: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(G) and is_integer_graph(G)

    s: int = get_only(sources(G))
    longest_path_lengths: dict[int, float] = single_source_longest_dag_path_length(G, s)

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

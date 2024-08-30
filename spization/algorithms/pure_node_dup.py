from typing import Iterator
from networkx import DiGraph
import networkx as nx
from spization.sp_utils.serial_parallel_decomposition import SerialParallelDecomposition
from spization.sp_utils.compositions import sp_serial_composition, sp_parallel_composition
from spization.sp_utils.normalize import normalize
from spization.utils.graph_utils import sources, sinks, is_2_terminal_dag, is_integer_graph
from spization.utils.general_utils import get_only

def pure_node_dup(g : DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_integer_graph(g)
    root = get_only(sources(g))
    node_to_sp : dict[int, SerialParallelDecomposition] = {root : root}
    for node in nx.topological_sort(g):
        if node==root: continue
        predecessors : Iterator[SerialParallelDecomposition] = g.predecessors(node)
        node_to_sp[node] = normalize(sp_serial_composition((sp_parallel_composition([node_to_sp.get(p) for p in predecessors]), node)))
        print(node_to_sp)
    sink : int = get_only(sinks(g))
    final : SerialParallelDecomposition = normalize(node_to_sp[sink])
    return final

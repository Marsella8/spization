from random import choice, random, sample
from spization.objects import PureNode, Serial, Parallel
from spization.utils.get_nodes import get_nodes
from spization.utils.replace_node import replace_node
from spization.utils.normalize import normalize

def get_random_node(sp):
    return choice(list(get_nodes(sp)))

def random_sp(num_nodes : int, prob_serial : float = 0.5):
    assert 0 <= prob_serial <= 1 and num_nodes > 0 
    sp = PureNode(0)
    for node in range(1,num_nodes):
        node_to_sub = get_random_node(sp)
        print(sp)
        print(node, node_to_sub)
        n1, n2 = sample((node_to_sub, node), 2) # For Serial
        if random() < prob_serial:
            sp = replace_node(sp, node_to_sub, Serial((n1, n2)))
        else:
            sp = replace_node(sp, node_to_sub, Parallel((n1, n2)))
    return normalize(sp)

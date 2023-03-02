from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import EpsilonNFA


def create_dfsm_by_regular_expression(regular: str):
    return Regex(regular).to_epsilon_nfa().to_deterministic().minimize()


# nondeterministic finite state machine
def create_ndfsm_by_graph(graph, start_vertex=None, end_vertex=None):
    if start_vertex is None:
        start_vertex = graph.nodes
    if end_vertex is None:
        end_vertex = graph.nodes
    ndfsm = EpsilonNFA().from_networkx(graph)
    for i in start_vertex:
        ndfsm.add_start_state(i)
    for i in end_vertex:
        ndfsm.add_final_state(i)
    return ndfsm

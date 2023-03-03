from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import EpsilonNFA


def create_dfsm_by_regular_expression(regular: str):
    """
        Builds a deterministic finite state machine using the resulting regular expression

    :param regular: string, which is a regular expression
    :return: deterministic finite state machine :class:`~pyformlang.deterministic_finite_automaton\
        .DeterministicFiniteAutomaton`
    """
    return Regex(regular).to_epsilon_nfa().minimize()


# nondeterministic finite state machine
def create_ndfsm_by_graph(graph, start_vertex=None, end_vertex=None):
    """
        Constructs a nondeterministic finite automaton over the graph

    :param graph: the graph representation of the automaton
    :param start_vertex: the vertices that are the starting values of the automaton
    :param end_vertex: the vertices that are finite values of the automaton
    :return: nondeterministic finite automaton :class:`~pyformlang.finite_automaton.NondeterministicTransitionFunction`
    """
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

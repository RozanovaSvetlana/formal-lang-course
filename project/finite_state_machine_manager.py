from pyformlang.regular_expression import Regex

from project.matrix_manager import *


def create_dfsm_by_regular_expression(regular: str):
    """
        Builds a deterministic finite state machine using the resulting regular expression

    :param regular: string, which is a regular expression
    :return: deterministic finite state machine :class:`~pyformlang.deterministic_finite_automaton\
        .DeterministicFiniteAutomaton`
    """
    return Regex(regular).to_epsilon_nfa().minimize()


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


def ap_rpq(graph, regular: str, start_vertex=None, end_vertex=None):
    """
    Performs regular graph queries: on a graph with given start and end vertices
    and a regular expression, return those pairs of vertices from the given start and end vertices
    that are connected by a path forming a word from the language given by the regular expression.
    :param graph: query graph
    :param regular:
    :param start_vertex: starting vertices of the graph
    :param end_vertex: final vertices of the graph
    :return: list of start and end nodes
    """
    graph_fst = create_ndfsm_by_graph(graph, start_vertex, end_vertex)
    graph_snd = create_dfsm_by_regular_expression(regular)
    boolean_matrix_fst = get_boolean_matrix(graph_fst)
    boolean_matrix_snd = get_boolean_matrix(graph_snd)
    result_transitive = transitive_closure(
        get_graph_intersection_by_matrix(boolean_matrix_fst, boolean_matrix_snd)
    )
    all_state_fst = {start: i for (i, start) in enumerate(graph_fst.states)}
    all_state_snd = {start: i for (i, start) in enumerate(graph_snd.states)}
    list_start = {}
    list_end = {}
    for index_fst in all_state_fst:
        for index_snd in all_state_snd:
            new_state = (
                all_state_fst[index_fst] * len(list(graph_snd.states))
                + all_state_snd[index_snd]
            )
            if (
                index_fst in graph_fst.start_states
                and index_snd in graph_snd.start_states
            ):
                list_start[new_state] = index_fst
            if (
                index_fst in graph_fst.final_states
                and index_snd in graph_snd.final_states
            ):
                list_end[new_state] = index_fst
    result = []
    for start, end in zip(*result_transitive.nonzero()):
        if start in list_start and end in list_end:
            result.append((list_start[start], list_end[end]))
    return result

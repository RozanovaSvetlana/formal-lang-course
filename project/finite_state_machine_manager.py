from collections import namedtuple

from pyformlang.finite_automaton import State, DeterministicFiniteAutomaton, EpsilonNFA
from pyformlang.regular_expression import Regex
from scipy.sparse import dok_matrix, vstack
from cfpq_data import *

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


def transform(matrix, length):
    """
        Transforms matrix to the mathix with only ones at the main diagonal

    :param matrix: front
    :param length: count of states in the second graph
    :return: transformed dok_matrix front
    """
    mathix_transformed = dok_matrix(matrix.shape, dtype=bool)
    for x, y in zip(*matrix.nonzero()):
        if y < length:
            row = matrix[[x], length:]
            if row.nnz > 0:
                shift = x - (x % length)
                mathix_transformed[shift + y, y] = True
                mathix_transformed[[shift + y], length:] += row
    return mathix_transformed


def front_each(fst_info, snd_info):
    """
        Calculates front for separated each start state

    :param fst_info: info about first graph
    :param snd_info: info about second graph
    :return: created front
    """
    front = None
    for s in fst_info.start_states:
        temp_front = dok_matrix(
            (
                len(snd_info.all_states),
                len(fst_info.all_states) + len(snd_info.all_states),
            ),
            dtype=bool,
        )
        r = dok_matrix((1, len(fst_info.all_states)), dtype=bool)
        r[0, fst_info.start_states[s]] = True
        for state in snd_info.start_states:
            i = snd_info.all_states[state]
            temp_front[i, i] = True
            temp_front[[i], len(snd_info.all_states) :] = r
        front = temp_front if front is None else vstack([front, temp_front])
    return front


def front_all(fst_info, snd_info):
    """
        Calculates front for not separated all states

    :param fst_info: info about first graph
    :param snd_info: info about second graph
    :return: created front
    """
    front = dok_matrix(
        (
            len(snd_info.all_states),
            len(fst_info.all_states) + len(snd_info.all_states),
        ),
        dtype=bool,
    )
    front_right = dok_matrix((1, len(fst_info.all_states)), dtype=bool)
    for s in fst_info.start_states:
        front_right[0, fst_info.start_states[s]] = True
    for s in snd_info.start_states:
        index = snd_info.all_states[s]
        front[index, index] = True
        front[[index], len(snd_info.all_states) :] = front_right
    return front


def BFS(fst_graph_info, snd_graph_info, for_each: bool):
    """
        BFS to calculate direct sums, fronts (for each or for all states) and perform bfs in cycle while front is changing

    :param fst_graph_info: boolean matrix, all states, final and start states for the first graph
    :param snd_graph_info: boolean matrix, all states, final and start states for the second graph
    :param for_each: create front for all states (false) or for each (true)
    :return: all visited after bfs states
    """
    direct_sum = dict()
    for symbol in fst_graph_info.boolean_matrix:
        if symbol in snd_graph_info.boolean_matrix:
            direct_sum[symbol] = sparse.bmat(
                [
                    [snd_graph_info.boolean_matrix[symbol], None],
                    [None, fst_graph_info.boolean_matrix[symbol]],
                ]
            )

    front = (
        front_each(fst_graph_info, snd_graph_info)
        if for_each
        else front_all(fst_graph_info, snd_graph_info)
    )
    is_changed = True
    visited = dok_matrix(front.shape, dtype=bool)
    next = visited.nnz
    while is_changed:
        for key, value in direct_sum.items():
            if front is None:
                new_front = visited.dot(value)
            else:
                new_front = front.dot(value)
            visited += transform(new_front, len(snd_graph_info.all_states))
        is_changed = visited.nnz != next
        front = None
        next = visited.nnz
    return visited


def ms_rpq(graph, regex, start_vertex=None, end_vertex=None, for_each=True):
    graph_fst = create_ndfsm_by_graph(graph, start_vertex, end_vertex)
    graph_snd = create_dfsm_by_regular_expression(regex)

    graph_info = namedtuple(
        "graph_info", "boolean_matrix all_states start_states final_states"
    )

    def get_graph_info(g):
        """
        Return information about all states of graph, start states and final
        :param g: graph
        """
        boolean_matrix = get_boolean_matrix(g)
        all_state = {state: idx for (idx, state) in enumerate(g.states)}
        start_states = {State(state): state.value for state in g.start_states}
        final_states = {State(state): state.value for state in g.final_states}
        return graph_info(boolean_matrix, all_state, start_states, final_states)

    first_graph_info = get_graph_info(graph_fst)
    second_graph_info = get_graph_info(graph_snd)
    result = BFS(first_graph_info, second_graph_info, for_each)

    answer = set()

    f_all_keys = list(first_graph_info.all_states.keys())
    s_all_keys = list(second_graph_info.all_states.keys())
    f_all_values = list(first_graph_info.all_states.values())
    s_all_values = list(second_graph_info.all_states.values())

    for i, j in zip(*result.nonzero()):
        if j >= len(second_graph_info.all_states):
            i_first = j - len(second_graph_info.all_states)
            i_second = i % len(second_graph_info.all_states)
            x = f_all_keys[f_all_values[i_first]]
            y = s_all_keys[s_all_values[i_second]]
            if (
                x in first_graph_info.final_states.keys()
                and y in second_graph_info.final_states.keys()
            ):
                answer.add(
                    (State(i // len(second_graph_info.all_states)), State(i_first))
                    if for_each
                    else State(i_first)
                )

    return answer

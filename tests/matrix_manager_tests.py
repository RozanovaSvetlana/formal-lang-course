import cfpq_data

from project.finite_state_machine_manager import (
    create_dfsm_by_regular_expression,
    create_ndfsm_by_graph,
)
from project.matrix_manager import *


def get_boolean_matrix_test():
    matrix = get_boolean_matrix(
        create_ndfsm_by_graph(
            cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b"))
        )
    )
    assert list(matrix.keys()) == ["a", "b"]
    all_nnz = {"a": 3, "b": 4}
    for label in matrix.keys():
        assert matrix[label].getnnz() == all_nnz[label]


def transitive_closure_test():
    assert (
        transitive_closure(
            get_boolean_matrix(create_dfsm_by_regular_expression("a*"))["a"]
        ).getnnz()
        == 1
    )
    matrix = get_boolean_matrix(
        create_ndfsm_by_graph(
            cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b"))
        )
    )
    assert transitive_closure(matrix["a"]).getnnz() == 9
    assert transitive_closure(matrix["b"]).getnnz() == 16


def get_graph_intersection_by_matrix_test():
    fst = create_dfsm_by_regular_expression("a|b|c")
    snd = create_ndfsm_by_graph(
        cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b"))
    )
    assert (
        get_graph_intersection_by_matrix(
            get_boolean_matrix(fst), get_boolean_matrix(snd)
        ).getnnz()
        == 7
    )
    snd = create_dfsm_by_regular_expression("a*")
    assert (
        get_graph_intersection_by_matrix(
            get_boolean_matrix(fst), get_boolean_matrix(snd)
        ).getnnz()
        == 1
    )

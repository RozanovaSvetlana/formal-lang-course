import cfpq_data

from project.finite_state_machine_manager import *


def create_dfsm_by_regular_expression_test():
    graph = create_dfsm_by_regular_expression("(td)|(tc)|x")
    assert graph.accepts(["td"])
    assert not graph.accepts(["tdx"])
    assert graph.accepts(["x"])
    assert not graph.accepts(["asfas"])
    assert graph.accepts(["tc"])


def create_ndfsm_by_graph_test():
    cycles_graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b"))
    graph = create_ndfsm_by_graph(cycles_graph)
    assert graph.accepts(["a"])
    assert graph.accepts(["b"])
    assert not graph.accepts(["ab"])
    assert not graph.accepts(["bb"])
    assert not graph.accepts(["ba"])
    assert not graph.accepts(["sdfsd"])


def ap_rpq_test():
    assert ap_rpq(
        cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b")),
        "a|bb",
        {0},
        {1, 2, 3},
    ) == [(0, 1)]
    assert ap_rpq(
        cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b")),
        "a|b|c",
        {0},
        {1, 2, 3},
    ) == [(0, 1), (0, 3)]
    assert (
        ap_rpq(
            cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b")),
            "dsa",
            {0},
            {1, 2, 3},
        )
        == []
    )
    assert ap_rpq(
        cfpq_data.labeled_two_cycles_graph(2, 3, labels=("ac", "b")),
        "(ac|bc)|ac",
        {0},
        {1},
    ) == [(0, 1)]
    assert (
        ap_rpq(
            cfpq_data.labeled_two_cycles_graph(2, 3, labels=("ac", "b")),
            "(ac|bc)|ac",
            {0},
            {2, 3},
        )
        == []
    )

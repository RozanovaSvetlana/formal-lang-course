import cfpq_data
import pytest

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


@pytest.mark.parametrize(
    "cycle_count, start, final, labels, regex, result",
    [
        ([3, 1], [1, 4], [1, 2], ["0", "1"], "0|1.", {2}),
        ([3, 6], [0, 1, 2], [3, 4], ["0", "1"], "1*|0.1", {4}),
        ([4, 4], None, None, ["0", "1"], "0*1*", {0, 1, 2, 3, 4, 5, 6, 7, 8}),
    ],
)
def test_ms_rpq_1(cycle_count, start, final, labels, regex, result):
    graph = cfpq_data.labeled_two_cycles_graph(
        cycle_count[0], cycle_count[1], labels=labels
    )
    actual = ms_rpq(graph, regex, start, final, False)
    assert result == actual


@pytest.mark.parametrize(
    "cycle_count, start, final, labels, regex, result",
    [
        ([2, 3], [1, 2, 3], [4], ["0", "1"], "1|0*", {(2, 4)}),
        ([2, 1], [0, 1], [2], ["1", "2"], "2.(12)*", set()),
        (
            [2, 2],
            None,
            None,
            ["0", "1"],
            "0*.1*",
            {
                (4, 0),
                (3, 4),
                (4, 3),
                (0, 2),
                (2, 2),
                (1, 0),
                (1, 3),
                (3, 0),
                (3, 3),
                (0, 1),
                (2, 4),
                (1, 2),
                (0, 4),
                (2, 1),
                (4, 4),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 0),
                (1, 4),
                (2, 3),
            },
        ),
    ],
)
def test_ms_rpq_2(cycle_count, start, final, labels, regex, result):
    graph = cfpq_data.labeled_two_cycles_graph(
        cycle_count[0], cycle_count[1], labels=labels
    )
    actual = ms_rpq(graph, regex, start, final, True)
    assert result == actual

import cfpq_data
import pytest

from project import cfpq
from project.context_free_grammar import *


def test_cfg_into_weak_cnf():
    check_is_cfg_equals(
        cfg_into_weak_cnf("S -> a d\nB -> C\n C -> d\nC -> d"),
        get_cfg_from_text('S -> "VAR:a#CNF#" "VAR:d#CNF#"\nd#CNF# -> d\na#CNF# -> a\n'),
    )
    check_is_cfg_equals(
        cfg_into_weak_cnf("S -> A B\nA -> a\nB -> epsilon"),
        get_cfg_from_text("A -> a\nS -> A B\nB -> \n"),
    )


def test_get_cfg_from_file():
    # error path
    with pytest.raises(OSError):
        get_cfg_from_file("error_path")
    check_is_cfg_equals(
        get_cfg_from_file("tests/files_for_tests/simple_cfg.txt"), get_cfg_from_text("S -> a")
    )
    check_is_cfg_equals(
        get_cfg_from_file("tests/files_for_tests/some_cfg.txt"),
        get_cfg_from_text("S -> A B C D E\nA -> a\nB -> b\nC -> c\nD -> d\nE -> e"),
    )


def check_is_cfg_equals(cfg_actual: CFG, cfg_expected: CFG):
    assert cfg_actual.productions == cfg_expected.productions
    assert cfg_actual.start_symbol == cfg_expected.start_symbol
    assert cfg_actual.terminals == cfg_expected.terminals
    assert cfg_actual.variables == cfg_expected.variables


def test_context_free_path_queruing_by_hellinges_1():
    graph = cfpq_data.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    cfg = CFG.from_text("S -> a b")
    assert cfpq.hellings(graph, cfg) == {(2, 3)}


def test_context_free_path_queruing_by_hellinges_2():
    graph = cfpq_data.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    cfg = CFG.from_text("S -> a S | P\nP -> b P | b")
    assert cfpq.hellings(graph, cfg) == {(0, 0), (0, 3), (2, 0), (3, 0), (2, 3), (3, 3),
                                         (1, 0), (1, 3)}


def test_context_free_path_queruing_by_hellinges_3():
    graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a", "b"))
    cfg = CFG.from_text("S -> ( S ) S\nS -> S ( S )\nS -> epsilon")
    assert cfpq.hellings(graph, cfg) == {(4, 4), (5, 5), (0, 0), (1, 1), (3, 3), (2, 2)}

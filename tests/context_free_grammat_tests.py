import pytest

from project.context_free_grammar import *


def cfg_into_weak_cnf_test():
    check_is_cfg_equals(
        cfg_into_weak_cnf("S -> a d\nB -> C\n C -> d\nC -> d"),
        get_cfg_from_text('S -> "VAR:a#CNF#" "VAR:d#CNF#"\nd#CNF# -> d\na#CNF# -> a\n'),
    )
    check_is_cfg_equals(
        cfg_into_weak_cnf("S -> A B\nA -> a\nB -> epsilon"),
        get_cfg_from_text("A -> a\nS -> A B\nB -> \n"),
    )


def get_cfg_from_file_test():
    # error path
    with pytest.raises(OSError):
        get_cfg_from_file("error_path")
    check_is_cfg_equals(
        get_cfg_from_file("files_for_tests\simple_cfg.txt"), get_cfg_from_text("S -> a")
    )
    check_is_cfg_equals(
        get_cfg_from_file("files_for_tests\some_cfg.txt"),
        get_cfg_from_text("S -> A B C D E\nA -> a\nB -> b\nC -> c\nD -> d\nE -> e"),
    )


def check_is_cfg_equals(cfg_actual: CFG, cfg_expected: CFG):
    assert cfg_actual.productions == cfg_expected.productions
    assert cfg_actual.start_symbol == cfg_expected.start_symbol
    assert cfg_actual.terminals == cfg_expected.terminals
    assert cfg_actual.variables == cfg_expected.variables

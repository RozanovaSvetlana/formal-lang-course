import pytest
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG
from project.context_free_grammar import cfg_into_weak_cnf, get_cfg_from_text, get_cfg_from_file
from project.rsm import RSM


@pytest.mark.parametrize(
    "cfg",
    [
        "S -> A B \nA B -> B C B A \n B C -> A \n A -> epsilon",
        "S -> epsilon \n S -> Ba \n B -> aaS\n B -> a"
    ]
)
def test_from_cfg(cfg):
    weak_cfg = cfg_into_weak_cnf(get_cfg_from_text(cfg))
    ecfg = ECFG().from_cfg(weak_cfg)
    assert weak_cfg.variables == ecfg.vars
    assert weak_cfg.start_symbol == ecfg.start
    assert weak_cfg.terminals == ecfg.terminals


def test_from_string():
    ecfg = ECFG().from_string("S -> A\n S -> ab\n S -> epsilon\n A -> B \n B -> S\n B -> epsilon")
    productions = {
                    Variable("S"): Regex("A | ab | epsilon"),
                    Variable("B"): Regex("S | epsilon"),
                    Variable("A"): Regex("B"),
                }
    for head, body in ecfg.productions.items():
        expected = productions[head]
        assert body.to_epsilon_nfa().is_equivalent_to(expected.to_epsilon_nfa())


@pytest.mark.parametrize(
    "file, productions",
    [
        (
                "tests/files_for_tests/simple-ecfg",
                {
                    Variable("S"): Regex("B | a*b | epsilon"),
                    Variable("C"): Regex("S S"),
                    Variable("B"): Regex("C"),
                }
        ),
        (
                "tests/files_for_tests/example_ecfg",
                {
                    Variable("S"): Regex("S A"),
                    Variable("A"): Regex("a | B"),
                    Variable("B"): Regex("C | epsilon"),
                    Variable("C"): Regex("c"),
                }
        )
    ]
)
def test_from_file(file, productions):
    ecfg = ECFG().from_file(file)
    for head, body in ecfg.productions.items():
        assert body.to_epsilon_nfa().is_equivalent_to(productions[head].to_epsilon_nfa())


@pytest.mark.parametrize(
    "s, expected",
    [
        ("S -> A\n S -> ab\n S -> epsilon\n A -> B \n B -> S\n B -> epsilon", "tests/files_for_tests/simple_ecfg_result"),
        ("S -> AaA\nA -> b | B | b\nB -> S\nB -> epsilon\n", "tests/files_for_tests/simple_ecfg_result_2")
    ],
)
def test_minimize(s, expected):
    ecfg = ECFG().from_string(s)
    actual = RSM().from_ecfg(ecfg).minimize()
    expected_ecfg = ECFG().from_cfg(get_cfg_from_file(expected))
    expected = RSM().from_ecfg(expected_ecfg)

    for head, body in expected.productions.items():
        assert body.is_equivalent_to(actual.productions[head])


@pytest.mark.parametrize(
    "ecfg, expected",
    [
        ("S -> A\n S -> ab\n S -> epsilon\n A -> B \n B -> S\n B -> epsilon", "tests/files_for_tests/simple_ecfg_result"),
        ("S -> AaA\nA -> b | B | b\nB -> S\nB -> epsilon\n", "tests/files_for_tests/simple_ecfg_result_2"),
    ],
)
def test_from_ecfg(ecfg, expected):
    ecfg = ECFG().from_string(ecfg)
    rsm = RSM().from_ecfg(ecfg)
    expected_ecfg = ECFG().from_cfg(get_cfg_from_file(expected))
    expected = RSM().from_ecfg(expected_ecfg)
    assert rsm.productions == expected.productions

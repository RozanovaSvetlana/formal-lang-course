from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable


def cfg_into_weak_cnf(cfg, start_symbol=Variable("S")) -> CFG:
    """
        Translation of context-free grammar
        into weak Chomsky's normal form
    :param cfg: context-free grammar as object or as a string
    :param start_symbol: start symbol, S by default, for cfg as a string
    :return: contex free grammar into wcnf
    """
    if isinstance(cfg, str):
        cfg = get_cfg_from_text(cfg, start_symbol)
    start_symbol = cfg.start_symbol
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    cfg = cfg._decompose_productions(cfg._get_productions_with_only_single_terminals())
    return CFG(start_symbol=start_symbol, productions=set(cfg))


def get_cfg_from_text(cfg: str, start_symbol=Variable("S")) -> CFG:
    """
        Utility method for easy operation when translating a cfg from text to object
    :param cfg: context-free grammar as a string
    :param start_symbol: start symbol, S by default
    :return: contex free grammar
    """
    return CFG.from_text(cfg, start_symbol)


def get_cfg_from_file(file_name: str, start_symbol=Variable("S")) -> CFG:
    """
        Get context free grammar from file

    :param file_name: file name for read
    :param start_symbol: start symbol, S by default
    :return: contex free grammar
    """
    text = ""
    with open(file_name, "r") as file:
        text = file.read()
    return get_cfg_from_text(text, start_symbol)


def hellinges(graph: MultiDiGraph, cfg: CFG):
    """
        Finds paths in the graph between vertices according
        to the conditions of grammar with the help
        of the Hellings algorithm
    :param graph: the graph representation of the automaton
    :param cfg: context-free grammar as object
    :return: a set of triples of a species (non-terminus, vertex, vertex).
    """
    cfg = cfg_into_weak_cnf(cfg)
    r = {
        (nt, v, v)
        for v in graph.nodes
        for nt in {i.head.value for i in cfg.productions if not i.body}
    } | {
        (nt.head.value, v, u)
        for (v, u, t) in graph.edges(data="label")
        for nt in {i for i in cfg.productions if len(i.body) == 1}
        if nt.body[0].value == t
    }
    m = r.copy()
    nt = {i for i in cfg.productions if len(i.body) == 2}
    while m:
        nti, v, u = m.pop()
        for (ntj, vs, _) in {i for i in r if i[2] == v}:
            for trio in {
                (i.head.value, vs, u)
                for i in nt
                if (i.head.value, vs, u) not in r
                and i.body[0].value == ntj
                and i.body[1].value == nti
            }:
                m |= {trio}
                r |= {trio}
        for (ntj, _, us) in {i for i in r if i[1] == u}:
            for trio in {
                (i.head.value, v, us)
                for i in nt
                if (i.head.value, v, us) not in r
                and i.body[0].value == nti
                and i.body[1].value == ntj
            }:
                m |= {trio}
                r |= {trio}
    return r


def context_free_path_queruing_by_hellinges(
    graph: MultiDiGraph,
    cfg: CFG,
    start_vertex=None,
    end_vertex=None,
    start_symbol=Variable("S"),
):
    """
        Based on the Hellings algorithm solves the reachability problem
    :param graph: the graph representation of the automaton
    :param cfg: context-free grammar as object
    :param start_vertex: the vertices that are the starting values of the automaton
    :param end_vertex: the vertices that are finite values of the automaton
    :param start_symbol: start symbol, S by default
    :return:
    """
    if start_vertex is None:
        start_vertex = graph.nodes
    if end_vertex is None:
        end_vertex = graph.nodes
    return {
        (v, u)
        for (nt, v, u) in hellinges(graph, cfg)
        if v in start_vertex and u in end_vertex and nt == start_symbol
    }

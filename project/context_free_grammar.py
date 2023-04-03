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
    cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
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

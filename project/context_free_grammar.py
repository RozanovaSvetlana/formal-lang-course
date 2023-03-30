from pyformlang.cfg import CFG, Variable


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
    return CFG.from_text(text, start_symbol)

from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.context_free_grammar import get_cfg_from_file


class ECFG:
    """
    Extended Context-Free Grammars
    """

    def __init__(self):
        self.productions = None
        self.vars = None
        self.start = None
        self.terminals = None

    def from_cfg(self, cfg):
        """
        Creates simple-ecfg from cfg
        """
        self.start = cfg.start_symbol if cfg.start_symbol else Variable("S")
        self.vars = set(cfg.variables)
        self.vars.add(self.start)
        self.terminals = cfg.terminals

        self.productions = dict()

        for production in cfg.productions:
            body = (
                Regex("$")
                if len(production.body) == 0
                else Regex("".join(" " + pr_body.value for pr_body in production.body))
            )
            self.productions[production.head] = (
                self.productions.get(production.head).union(body)
                if production.head in self.productions
                else body
            )
        return self

    def from_string(self, s):
        """
        Creates simple-ecfg from string
        """
        cfg = CFG.from_text(s)
        return self.from_cfg(cfg)

    def from_file(self, file):
        """
        Creates simple-ecfg from file
        """
        cfg = get_cfg_from_file(file)
        return self.from_cfg(cfg)

from project.ecfg import ECFG
from project.matrix_manager import get_boolean_matrix


class RSM:
    """
    Recursive state machine
    """

    def __init__(self):
        self.matrixes = dict()
        self.productions = dict()

    def minimize(self):
        for head, body in self.productions.items():
            self.productions[head] = body.minimize()
        return self

    def from_ecfg(self, ecfg: ECFG):
        for head, body in ecfg.productions.items():
            production = body.to_epsilon_nfa()
            self.productions[head] = production
            self.matrixes[head] = get_boolean_matrix(production)
        return self

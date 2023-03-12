from pyformlang.finite_automaton import EpsilonNFA
from scipy import sparse


def get_boolean_matrix(graph: EpsilonNFA):
    """
    Constructs a Boolean matrix on the fs

    :param graph: EpsilonNFA for constructing a boolean matrix
    :return: a boolean matrix
    """
    # answer
    matrix = {}
    # matrix dimensions for each marker
    len_states = len(graph.states)
    # to get the vertex index
    all_state = {start: i for (i, start) in enumerate(graph.states)}
    # iterating over the vertices of the graph
    for start_state, labels in graph.to_dict().items():
        # iterate along the edges that emerge from the vertex
        for edge, vertexes in labels.items():
            # a crutch for iteration, as there is no guarantee that the graph is minimal
            if not isinstance(vertexes, set):
                vertexes = {vertexes}
            for v in vertexes:
                # if an edge with this label has never been added, then add it to the response with the matrix
                if not edge in matrix:
                    matrix[edge] = sparse.dok_matrix(
                        (len_states, len_states), dtype=bool
                    )
                matrix[edge][all_state[start_state], all_state[v]] = True
    return matrix


def transitive_closure(matrix):
    """
    Makes a transitive closure of matrix
    :param matrix: closing matrix
    :return: closed matrix
    """
    all = matrix.getnnz()
    start = 0
    while start != all:
        matrix += matrix @ matrix
        start = all
        all = matrix.nnz
    return matrix


def get_graph_intersection_by_matrix(matrix_fst_fa, matrix_snd_fa):
    """
    Finds intersections of boolean matrices by labels,
    makes their kron multiplication and adds up all the results
    :param matrix_fst_fa: first boolean matrix
    :param matrix_snd_fa: second boolean matrix
    :return: boolean intersection matrix
    """
    intersection_labels = matrix_fst_fa.keys() & matrix_snd_fa.keys()
    shape_fst = matrix_fst_fa[list(matrix_fst_fa.keys())[0]].shape[0]
    shape_snd = matrix_snd_fa[list(matrix_snd_fa.keys())[0]].shape[0]
    shape_intersection = shape_fst * shape_snd
    matrix = sparse.dok_matrix((shape_intersection, shape_intersection), dtype=bool)
    for label in intersection_labels:
        matrix += sparse.kron(matrix_fst_fa[label], matrix_snd_fa[label])
    return matrix

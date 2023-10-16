from project.context_free_grammar import (
    context_free_path_querying_by_hellinges,
    context_free_path_querying_by_matrix,
)


def hellings(graph, cfg):
    return context_free_path_querying_by_hellinges(graph, cfg)


def matrix(graph, cfg):
    return context_free_path_querying_by_matrix(graph, cfg)

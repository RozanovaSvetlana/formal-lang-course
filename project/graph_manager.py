from typing import Tuple

import cfpq_data
import networkx


def get_graf_information_by_name(name: str):
    """
        Return information about graph: count vertex, count edges, all labels

    :param name: string which is the name of the graph
    :return: count vertex, count edges, all labels
    """
    graph = get_graph_by_name(name)
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_sorted_labels(graph),
    )


def get_graph_by_name(name: str):
    """
        Download and return graph

    :param name: string which is the name of the graph
    :return: download graph: nx.MultiDiGraph
    """
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def create_graph_by_number_vertices_in_loops_and_label_names_and_save_in_file(
    fst_nodes_count: int, snd_nodes_count: int, labels: Tuple[str, str], file_name: str
):
    """
        Constructs a graph of two cycles based on the number of vertices
        in the cycles and the label names and saves it to the specified
        file in DOT format

    :param fst_nodes_count: count vertex first cycle
    :param snd_nodes_count: count vertex second cycle
    :param labels: labels
    :param file_name: name of the file where the graph will be saved must be in .dot format
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        fst_nodes_count, snd_nodes_count, labels=labels
    )
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write(file_name)

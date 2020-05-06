# -*- coding: utf-8 -*-

import sys

import graphviz as gv

styles = {
    "graph": {
        "label": "Network Map",
        "fontsize": "16",
        "fontcolor": "white",
        "bgcolor": "#333333",
        "rankdir": "TB",
    },
    "nodes": {
        "fontname": "Helvetica",
        "shape": "circle",
        "fontcolor": "white",
        "color": "#006699",
        "style": "filled",
        "fillcolor": "#006699",
    },
    "edges": {
        "style": "dashed",
        "color": "green",
        "arrowhead": "open",
        "fontname": "Courier",
        "fontsize": "14",
        "fontcolor": "white",
    },
}


def apply_styles(graph, styles):
    graph.graph_attr.update(("graph" in styles and styles["graph"]) or {})
    graph.node_attr.update(("nodes" in styles and styles["nodes"]) or {})
    graph.edge_attr.update(("edges" in styles and styles["edges"]) or {})
    return graph


def draw_topology(topology_dict, dest_filename="img/topology"):
    """
    topology_dict - словарь с описанием топологии
    Этот словарь
        {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
         ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
    соответствует топологии:
    [ R5 ]-Fa0/1 --- Fa0/1-[ R4 ]-Fa0/2---Fa0/0-[ R6 ]
    Функция генерирует топологию, в формате svg.
    И записывает файл topology.svg в каталог img.
    """
    nodes = set(
        [item[0] for item in list(topology_dict.keys()) + list(topology_dict.values())]
    )

    g1 = gv.Graph(format="svg")

    for node in nodes:
        g1.node(node)

    for key, value in topology_dict.items():
        head, t_label = key
        tail, h_label = value
        g1.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" " * 12)

    g1 = apply_styles(g1, styles)
    filename = g1.render(filename=dest_filename)
    print("Graph saved in", dest_filename)
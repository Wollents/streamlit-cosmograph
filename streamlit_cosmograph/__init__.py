import os

from streamlit_cosmograph.utils import get_node_position_colors

import streamlit.components.v1 as components


_RELEASE = False
if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _cosmo_graph = components.declare_component(
        "cosmo_graph",
        path=build_dir)
else:

    _cosmo_graph = components.declare_component("cosmo_graph", url="http://localhost:3001")


def cosmo_graph(nodes, links, configs, key=None):
    node_position = []
    colors = []
    links_list = []
    if nodes is not None:
        node_position, colors = get_node_position_colors(nodes, configs)
    if links is not None:
        for link in links:
            links_list.append(link.source)
            links_list.append(link.target)

    components_value = _cosmo_graph(nodes=node_position, links=links_list, colors=colors, configs=configs, default=None, key=key)
    return components_value
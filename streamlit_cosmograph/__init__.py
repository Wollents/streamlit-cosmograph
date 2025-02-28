#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: __init__.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:38 
@Last Modified by: yangwang0222@163.com
@Description : This file is used to prepare the component from the frontend.
               It is important to know that the function _cosmo_graph() is the main function of the component.
'''


import os

from streamlit_cosmograph.utils import get_node_position_colors

import streamlit.components.v1 as components


_RELEASE = True
if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _cosmo_graph = components.declare_component(
        "cosmo_graph",
        path=build_dir)
else:

    _cosmo_graph = components.declare_component("cosmo_graph", url="http://localhost:3001")


def cosmo_graph(nodes, links, configs, key=None):
    """
    Initailize the cosmograph component from the frontend.

    Arguments:
        nodes -- List[streamlit_cosmograph.node.Node]: List of nodes.
        links -- List[streamlit_cosmograph.link.Link]: List of links.
        configs -- dict:which contains the configs of the cosmograph component.

        key -- str: which is the identifier of declaring the component.

    Returns:
        value return from the frontend.
    """    
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
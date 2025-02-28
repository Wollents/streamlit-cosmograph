#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: utils.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:44 
@Last Modified by: yangwang0222@163.com
@Description: This module provides a variety of utility functions and methods aimed at simplifying the tasks of loading, processing, 
              and generating layouts for graph data. It supports importing network structure data from .mat and .json format files 
              and is capable of assigning position coordinates and colors to nodes for visualization purposes.

              Key features include:
                - Data Loading: Reads graph data (such as adjacency matrices, node labels, etc.) from uploaded .mat or .json files.

                - Graph Structure Generation: Automatically generates graph nodes and edges information based on input data, 
                                              supporting the generation of random graphs from test data.

                - Layout Algorithms: Offers three different layout algorithms - random layout, circular layout, and category-based 
                                     layout for nodes, assisting users in better understanding and presenting graph data.
                                     
                - Color Mapping: Generates color mappings for different categories of nodes, making it easier to distinguish between 
                                 types of nodes during visualization.

'''


import json
import random


import numpy as np
import scipy.io as sio
import scipy.sparse as sp


from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_cosmograph.node import Node
from streamlit_cosmograph.link import Link
from streamlit_cosmograph.layout import LayoutEnum


BASE_POS = 4096


def load_data_from_upload(uploaded_file: UploadedFile):
    post_fix = uploaded_file.name.split('.')[-1]
    if post_fix == 'mat':
        return load_mat_data(uploaded_file)

    elif post_fix == "json":
        return load_json_data(uploaded_file)
    else:
        raise Exception('Unsupported file format')


def load_mat_data(uploaded_file: str | UploadedFile):
    data = sio.loadmat(uploaded_file)
    selected_dataset = uploaded_file
    if isinstance(uploaded_file, UploadedFile):
        selected_dataset = uploaded_file.name

    adj = data['Network']
    num_nodes = adj.shape[0]
    adj_sp = sp.csr_matrix(adj)
    row, col = adj_sp.nonzero()
    links = []
    nodes = []
    for i in range(len(row)):
        links.append(Link(float(row[i]), float(col[i])))
    label = data['Label'] if ('Label' in data) else data.get('gnd', None)

    label = np.squeeze(label).tolist() if label is not None else None
    nodes = get_mat_nodes_list(num_nodes, label)
    graph_configs = data['GraphConfigs'] if ('GraphConfigs' in data) else {}

    return selected_dataset, nodes, links, graph_configs


def get_mat_nodes_list(num_nodes, label=None):

    return __generate_random_mat(num_nodes, label)


def __generate_random_mat(n_nodes, label):
    nodes = []
    unique_label = list(set(label))
    color_map = get_color_map(unique_label)
    for i in range(n_nodes):
        x = np.random.uniform(0, 1)
        y = np.random.uniform(0, 1)
        if label is not None:
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, label=label[i], colors=color_map.get(label[i])))
        else:
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, colors=[0, 255, 0, 1]))
    return nodes


def generate_circular_layout(nodes: list[Node]):
    n_nodes = len(nodes)

    radius = 0.5
    center = 0.5
    angle_step = 2 * np.pi / n_nodes
    node_position = []
    colors = []
    for i, node in enumerate(nodes):
        angle = i * angle_step
        node.x = center + radius * np.cos(angle)
        node.y = center + radius * np.sin(angle)
        node_position.extend([node.x, node.y])
        colors.extend(node.colors)

    return node_position, colors


def generate_bylabel_layout(nodes: list[Node]):

    unique_labels = list(set([node.label for node in nodes if node.label is not None]))
    num_classes = len(unique_labels)
    if num_classes < 2:
        return None

    region_width = 1.0 / num_classes
    nodes_posisitions = []
    colors = []
    color_map = get_color_map(unique_labels)

    for node in nodes:
        label = node.label
        if label is None:
            nodes_posisitions.extend([node.x, node.y])
            colors.extend([0, 255, 0, 1])
            continue

        # find current label index
        label_index = unique_labels.index(label)

        x_min = label_index * region_width
        x_max = (label_index + 1) * region_width

        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(0, 1)

        node.x = x * BASE_POS * region_width
        node.y = y * BASE_POS
        node.colors = color_map.get(label)

        colors.extend(node.colors)
        nodes_posisitions.extend([node.x, node.y])

    return nodes_posisitions, colors


def generate_random_layout(nodes: list[Node]):
    nodes_posisitions = []
    colors = []

    for node in nodes:
        node.x = np.random.uniform(0, 1) * BASE_POS
        node.y = np.random.uniform(0, 1) * BASE_POS
        colors.extend(node.colors)
        nodes_posisitions.extend([node.x, node.y])

    return nodes_posisitions, colors


def get_color_map(unique_labels):
    num_classes = len(unique_labels)
    color_map = {}
    if num_classes >= 2:
        color_map[unique_labels[0]] = [0, 255, 0, 1]  # 红色
        color_map[unique_labels[1]] = [255, 0, 0, 1]  # 绿色
        for i in range(2, num_classes):
            color_map[unique_labels[i]] = [
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                1
            ]
    else:
        color_map[unique_labels[0]] = [0, 255, 0, 1]  # 单类用蓝色
    return color_map


def load_test_data():
    return __generate_test_data()


def load_json_data(file: str | UploadedFile):
    nodes = []
    links = []
    name = None
    if isinstance(file, UploadedFile):
        file = file.read()
        test_file = json.loads(file)
        file_nodes = test_file['nodes']
        file_links = test_file['links']
        name = test_file['name']
        for node in file_nodes:
            nodes.append(Node(node['id'], x=node.get('x', random.uniform(0, 100)), y=node.get(
                'y', random.uniform(0, 100)), label=node['label'], colors=node['colors']))
        for link in file_links:
            links.append(Link(link['source'], link['target']))
        graph_configs = test_file['config'] if 'config' in test_file else {}

        return name, nodes, links, graph_configs

    with open(file, encoding="utf-8") as f:
        test_file = json.loads(f.read())
        file_nodes = test_file['nodes']
        file_links = test_file['links']
        name = test_file['name']
        for node in file_nodes:
            nodes.append(Node(node['id'], x=node.get('x', random.uniform(0, 100)), y=node.get(
                'y', random.uniform(0, 100)), label=node['label'], colors=node['colors']))
        for link in file_links:
            links.append(Link(link['source'], link['target']))
        graph_configs = test_file['config'] if 'config' in test_file else {}

    return name, nodes, links, graph_configs


def __generate_test_data(n: int = 100, m: int = 100, seed: int = 0):
    """generate random test data
        ref: https://stackblitz.com/edit/how-to-use-cosmos
    """
    nodes = []
    point_positions = []
    random.seed(seed)
    for point_index in range(n * m):
        x = 4096 * random.uniform(0.495, 0.505)
        y = 4096 * random.uniform(0.495, 0.505)
        point_positions.extend([x, y])
        nodes.append(Node(point_index, x=x, y=y))

    # links
    links_list = []
    links = []
    for point_index in range(n * m):
        next_point_index = point_index + 1
        bottom_point_index = point_index + n

        point_line = point_index // n
        next_point_line = next_point_index // n
        bottom_point_line = bottom_point_index // n

        # horizontal
        if point_line == next_point_line and next_point_index < n * m:
            links_list.append([point_index, next_point_index])
            links.append(Link(point_index, next_point_index))

        # vertical
        if bottom_point_line < m:
            links_list.append([point_index, bottom_point_index])
            links.append(Link(point_index, bottom_point_index))
    configs = {
        "simulation": True
    }
    name = "test_data"

    # return
    return name, nodes, links, configs


def get_node_position_colors(nodes: list[Node], config: dict):
    layout = config.get("layout")
    if layout == LayoutEnum.RANDOM:
        return generate_random_layout(nodes)
    elif layout == LayoutEnum.CIRCULAR:
        return generate_circular_layout(nodes)
    elif layout == LayoutEnum.BYLABEL:
        res = generate_bylabel_layout(nodes)
        if res is not None:
            return res

    node_position = []
    colors = []
    for node in nodes:
        node_position.append(node.x if node.x is not None else random.uniform(0,100))
        node_position.append(node.y if node.y is not None else random.uniform(0,100))
        colors.extend(node.colors)
    return node_position, colors

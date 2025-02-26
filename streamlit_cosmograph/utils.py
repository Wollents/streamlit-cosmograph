
import json
import numpy as np
import scipy.io as sio
import scipy.sparse as sp
from node import Node
from link import Link
from streamlit.runtime.uploaded_file_manager import UploadedFile
from layout import LayoutEnum

BASE_POS = 4096
def load_data_from_upload(uploaded_file: UploadedFile, layout=LayoutEnum.RANDOM):
    post_fix = uploaded_file.name.split('.')[-1]
    if post_fix == 'mat':
        data = sio.loadmat(uploaded_file)
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
        nodes = get_layout_nodes_position(layout, num_nodes, label)
    
        return selected_dataset, nodes, links
    
    elif post_fix == "json":
        pass
    else:
        raise Exception('Unsupported file format')
    
def get_layout_nodes_position(layout, num_nodes, label):

    if layout == LayoutEnum.CIRCULAR:
        return generate_circular_layout(num_nodes, label)
    if layout == LayoutEnum.RANDOM:
        return generate_random_layout(num_nodes, label)
    if layout == LayoutEnum.BYLABEL and label is not None:
        return generate_bylabel_layout(label)
    
def generate_random_layout(n_nodes, label):
    nodes = []

    for i in range(n_nodes):
        x = np.random.uniform(0, 1)
        y = np.random.uniform(0, 1)
        if label is not None:
            color_map = get_color_map(label)
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, label=label[i], colors=color_map.get(label[i])))
        else:
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, colors=[0, 255, 0, 1]))
    return nodes

def generate_circular_layout(n_nodes, labels=None):
    nodes = []
    radius = 0.5
    center = 0.5
    angle_step = 2 * np.pi / n_nodes

    for i in range(n_nodes):
        angle = i * angle_step
        x = center + radius * np.cos(angle)
        y = center + radius * np.sin(angle)
        if labels is not None:
            color_map = get_color_map(labels)
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, label=labels[i], colors=color_map.get(labels[i])))
        else:
            nodes.append(Node(i, x=x * BASE_POS, y=y * BASE_POS, colors=[0, 255, 0, 1]))
    return nodes

def generate_bylabel_layout(labels):
    nodes = []
    unique_labels = list(set(labels))
    num_classes = len(unique_labels)
    region_width = 1.0 / num_classes  # 每个标签占据的宽度比例
    for i, label in enumerate(labels):
        # 找到当前标签的索引
        label_index = unique_labels.index(label)
        
        # 计算当前标签的区域范围
        x_min = label_index * region_width
        x_max = (label_index + 1) * region_width
        
        # 在区域内随机生成节点的位置
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(0, 1)  # y 方向可以随机分布
        
        # 获取颜色映射
        color_map = get_color_map(labels)
        
        # 创建节点对象
        nodes.append(Node(
            id=i,
            x=x * BASE_POS * region_width,
            y=y * BASE_POS,
            label=label,
            colors=color_map.get(label)
        ))
    
    return nodes

def get_color_map(labels):
    unique_labels = list(set(labels))
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
    nodes = []
    links = []
    name = None
    import os
    with open('./data/test_data.json', encoding="utf-8") as f:
        test_file = json.loads(f.read())
        file_nodes = test_file['nodes']
        file_links = test_file['links']
        name = test_file['name']
        for node in file_nodes:
            nodes.append(Node(node['id'], x=node['x'], y=node['y'], label=node['label'], colors=node['colors']))
        for link in file_links:
            links.append(Link(link['source'], link['target']))
    return name, nodes, links
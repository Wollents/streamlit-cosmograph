import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import scipy.io as sio
import scipy.sparse as sp
import numpy as np
from node import Node
from link import Link
from utils import load_data_from_upload, load_test_data
_cosmo_graph = components.declare_component("cosmo_graph", url="http://localhost:3000")
cache_label = None
def get_random(min_val, max_val):
    return float(np.random.rand() * (max_val - min_val) + min_val)
def configure_sidebar() -> None:
    with st.sidebar:
        st.header("Information")
        st.info("This is a simple graph visualization tool.")
        st.header("Configuration")
        basic_configs = basic_expander()
        layout = layout_expander()
        selected_dataset, nodes, links = choose_dataset(layout)
        basic_configs["layout"] = layout
        return selected_dataset, nodes, links, basic_configs
    

def basic_expander(): 
    with st.expander("Basic Settings"):
        node_size = st.slider("Select node size", 0, 100, 10)
        link_size = st.slider("Select links size", 0, 100, 10)
        bg_color = st.color_picker("Select background color", "#000000")
        basic = {"background": bg_color, "nodeSize": node_size, "linkSize": link_size}
        return basic

def choose_dataset(layout="random"):
    with st.expander("Choose/upload Dataset To Visualize"):
        dataset_options = ("test_data")
        selected_dataset = st.selectbox(
            label="Choose your dataset:",
            options=dataset_options,
        )
        upload_file = st.file_uploader(label="Upload your own dataset", type=["mat", "json"])
        nodes, links = None, None
        if upload_file is not None:
            selected_dataset, nodes, links = load_data_from_upload(upload_file, layout)
        else:
            selected_dataset, nodes, links = load_test_data()
            
        return selected_dataset, nodes, links
    
def layout_expander():
    with st.expander("Choose a Layout"):
        layout_options = ("Random", "Circular", "ByLabel")
        selected_layout = st.selectbox(
            label="Choose your layout:",
            options=layout_options,
        )
        return selected_layout

st.set_page_config(
    page_title="Stable Diffusion WebUI",
    page_icon="",
    layout="wide",
)

def cosmo_graph(nodes, links, configs, key=None):
    node_position = []
    colors = []
    links_list = []
    if nodes is not None:
        for node in nodes:
            node_position.append(node.x)
            node_position.append(node.y)
            colors.extend(node.colors)
    if links is not None:
        for link in links:
            links_list.append(link.source)
            links_list.append(link.target)
    
    components_value = _cosmo_graph(nodes=node_position, links=links_list, colors=colors, configs=configs, default=None, key=key)
    return components_value


selected_dataset, nodes, links, configs = configure_sidebar()
st.header(f"{selected_dataset} Graph")

with st.container(border=True):
    return_value = cosmo_graph(nodes, links, configs, key=selected_dataset)

    if return_value is not None:
        target_node_id = return_value["node"]
        neighbor_id = return_value["neighbor"]
        target_node_label = nodes[target_node_id].label
        neighbor_label = []
        for n_id in neighbor_id:
            neighbor_label.append(nodes[n_id].label)
       

        st.markdown(f'''
                    **Selected Node id**: {target_node_id} 

                    **Selected Node label**: {target_node_label} 
                    
                    **Neighbor Node id**: {neighbor_id} 

                    **Neighbor Node label**: {neighbor_label}

                    ''')
    else:
        st.markdown("No node selected")
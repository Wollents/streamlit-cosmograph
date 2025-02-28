#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: config.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:43 
@Last Modified by: yangwang0222@163.com
@Description : This file is used to configure the sidebar and load test data.
'''


import streamlit as st


from streamlit_cosmograph.utils import load_data_from_upload, load_test_data


def configure_and_load() -> None:
    with st.sidebar:
        st.header("Information")
        st.info(
            "This is a simple graph visualization tool by cosmograph and streamlit. \n\n :bulb: It empowers you to smoothly visualize :red[10 Thousands-scale] nodes and edges in graph data.")
        st.header("Configuration")
        layout, on = layout_expander()
        basic_configs = basic_expander()
        selected_dataset, nodes, links, graph_config = load_dataset()
        basic_configs['layout'] = layout
        basic_configs['simulation'] = on
        graph_config.update(basic_configs)  # the system will overwrite the graph configs
        return selected_dataset, nodes, links, graph_config


def basic_expander():
    with st.expander("Basic Settings", expanded=True):
        node_size = st.slider("Select node size", 0, 100, 10)
        link_size = st.number_input("Input links size", 0.1)
        bg_color = st.color_picker("Select background color", "#000000")
        frame_height = st.slider("Select frame height", 0, 1000, 600)
        basic = {"backgroundColor": bg_color, "pointSize": node_size, "linkWidth": link_size, "frameHeight": frame_height}
        return basic


def load_dataset():
    with st.expander("Choose/upload Dataset To Visualize"):
        dataset_options = ("test_data")
        selected_dataset = st.selectbox(
            label="Choose your dataset:",
            options=dataset_options,
        )
        upload_file = st.file_uploader(label="Upload your own dataset", type=["mat", "json"])
        nodes, links = None, None
        if upload_file is not None:
            selected_dataset, nodes, links, graph_configs = load_data_from_upload(upload_file)
        else:
            selected_dataset, nodes, links, graph_configs = load_test_data()

        return selected_dataset, nodes, links, graph_configs


def layout_expander():
    with st.expander("Choose a Layout", expanded=True):
        on = st.toggle("Activate Graph Play When layout", value=True,
                       help="If activated, the graph will play automatically. \n\n If not, the graph will be :red[static] according to the :red[node's position].")
        layout_options = ("Origin", "Random", "Circular", "ByLabel")
        selected_layout = st.selectbox(
            label="Choose your layout:",
            options=layout_options
        )
        return selected_layout, on

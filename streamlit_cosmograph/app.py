#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: app.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:42 
@Last Modified by: yangwang0222@163.com
@Description : This is the basic app which is used to show how the streamlit-cosmograph works.
'''


import streamlit as st


from streamlit_cosmograph import cosmo_graph
from streamlit_cosmograph.config import configure_and_load

st.set_page_config(
    page_title="streamlit cosmograph",
    page_icon="",
    layout="wide",
)
selected_dataset, nodes, links, configs = configure_and_load()

st.markdown("# :rainbow[Streamlit Cosmograph]")
st.header(f":blue[{selected_dataset}] Graph :sparkles: (Node: {len(nodes)}, Links: {len(links)}) ", divider="grey")
with st.container(border=True):
    return_value: map = cosmo_graph(nodes, links, configs, key=selected_dataset)

if return_value is not None and len(return_value) > 0:
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

import os


import streamlit.components.v1 as components
import streamlit as st


from config import configure_and_load

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


if not _RELEASE:
    
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

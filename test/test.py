import pandas as pd
from cosmograph import cosmo
import streamlit as st
import streamlit.components.v1 as components
points = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'label': ['Node A', 'Node B', 'Node C', 'Node D', 'Node E'],
    'value': [10, 20, 15, 25, 30],
    'category': ['A', 'B', 'A', 'B', 'A']
})

links = pd.DataFrame({
    'source': [1, 2, 3, 1, 2],
    'target': [2, 3, 4, 5, 4],
    'value': [1.0, 2.0, 1.5, 0.5, 1.8]
})

widget = cosmo(
  points=points,
  enable_drag=True,
  links=links,
  point_id_by='id',
  link_source_by='source',
  link_target_by='target',
  point_color_by='category',
  point_include_columns=['value'],
  point_label_by='label',
  link_include_columns=['value'],
)
components.iframe(widget)
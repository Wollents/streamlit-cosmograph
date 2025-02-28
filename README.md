<h1 align="center"> <p>Streamlit Cosmograph</p></h1>
<h3 align="center">
<p>Streamlit wrapper of <a herf="https://cosmograph.app/" >Cosmographv2.0.</a> </p>
  <p>An Efficient Graph Visualiation Tool Tntegrated with Streamlit for Large Scale(10<sup>5</sup>~10<sup>6</sup>) Data</p>
</h3>

## Introduction

With Streamlit-Cosmograph, you can easily visualize your graogh data with a graph using Streamlit. It means you can  visualize your graogh data into web apps without the need to worry about the front-end code. Also, this repo provides a Example APP incuding functionalities like:

- Changing the basic configs.

- Support upload file.

- Custom Layout.


## Quick Install

`pip install streamlit-cosmograph`

## Example App
Check out the LIVE [Example App](https://github.com/streamlit/streamlit-cosmograph/blob/main/example_app.py)!!

## Basic Usage
```python
from streamlit_cosmograph import cosmo_graph
from streamlit_cosmograph.node import Node
from streamlit_cosmograph.link import Link


nodes = [Node(id=i, label=f"Node {i}") for i in range(1, 1001)]
links = [Link(source=i, target=i+1) for i in range(1, 1000)]
configs = {"linkWidth":1, "linkColor":"#696969", "pointSize": 3, "simulation":False}
return_value = cosmo_graph(nodes, links, configs)
```
And you will find the graph below:
<p style="text-align:center">
  <img src="imgs/code_exp.png" alt="code_exp" width="450" />
</p>

## Development and Run Locally


### Install

`git clone https://github.com/Wollents/streamlit-cosmograph.git`

- JS side

```shell script
cd streamlit_cosmograph/frontend/

npm install
```

- Python side
```shell script
cd streamlit_cosmograph/
python setup.py develop
```


### Run Locally

- JS side

```shell script
cd streamlit_cosmograph/frontend/

npm start
```

--Python side
```shell script
cd streamlit_cosmograph/
streamlit run app.py
```
And you will find the Web UI below:
![app_show.png](imgs/app_show.png)

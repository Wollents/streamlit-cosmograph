import json
import random
from typing import List, Dict, Any
from node import Node
from link import Link

def get_random(min_val: float, max_val: float) -> float:
    """生成指定范围内的随机数"""
    return random.uniform(min_val, max_val)

def generate_data(n: int = 100, m: int = 100) -> Dict[str, Any]:
    """生成节点和链接数据"""
    # 生成节点位置
    nodes = []
    point_positions = []
    for point_index in range(n * m):
        x = 4096 * get_random(0.495, 0.505)
        y = 4096 * get_random(0.495, 0.505)
        point_positions.extend([x, y])
        nodes.append(Node(point_index, x=x, y=y).to_dict())
    
    # 生成链接
    links_list = []
    links = []
    for point_index in range(n * m):
        next_point_index = point_index + 1
        bottom_point_index = point_index + n
        
        point_line = point_index // n
        next_point_line = next_point_index // n
        bottom_point_line = bottom_point_index // n
        
        # 水平链接
        if point_line == next_point_line and next_point_index < n * m:
            links_list.append([point_index, next_point_index])
            links.append(Link(point_index, next_point_index).to_dict())
        
        # 垂直链接
        if bottom_point_line < m:
            links_list.append([point_index, bottom_point_index])
            links.append(Link(point_index, bottom_point_index).to_dict())
    
    
    # 返回结果
    return {
        "nodes": nodes,
        "links": links,
        "config":{

        }
    }

def save_to_json(data: Dict[str, Any], filename: str = "data.json") -> None:
    """将数据保存为 JSON 文件"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # 生成数据
    data = generate_data(n=100, m=100)
    
    # 保存为 JSON 文件
    save_to_json(data, filename="grid_data.json")
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: node.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:44 
@Last Modified by: yangwang0222@163.com
@Description : node definition.
'''


class Node:
    def __init__(self, id, colors="#FDD2BS", label=None, x=None, y=None, **kwargs):
        self.id = id
        if label is None:
            self.label = str(id)
        else:
            self.label = label
        self.x = x
        self.y = y
        self.colors = colors
        self.__dict__.update(**kwargs)

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other) -> bool:
        return (isinstance(other, self.__class__) and
                getattr(other, 'id', None) == self.id)

    def __hash__(self) -> int:
        return hash(self.id)

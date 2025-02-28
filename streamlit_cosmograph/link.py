#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: link.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:43 
@Last Modified by: yangwang0222@163.com
@Description : Link definition.
'''


class Link:

    def __init__(self, source, target, **kwargs):
        self.source = source
        self.target = target
        self.__dict__.update(**kwargs)

    def to_dict(self):
        return self.__dict__

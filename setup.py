#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: setup.py
@Author: Wang Yang
@Email: yangwang0222@163.com
@Date:   2025/02/28 15:37 
@Last Modified by: yangwang0222@163.com
@Description : this file is used to setup the package.
'''


import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# python setup.py sdist bdist_wheel
# python -m twine upload  dist/*

setuptools.setup(
    license="MIT",
    name="streamlit_cosmograph",
    version="0.1.0",
    author="Wollents(Wang Yang)",
    author_email="yangwang0222@163.com",
    description="Cosmograph for Streamlit.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wollents/streamlit-cosmograph.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "streamlit >= 0.63",
        "scipy >= 1.4.1"
    ]
)
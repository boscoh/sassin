#!/usr/bin/env python
from setuptools import setup

description = \
"""`sassin` is a Python compiler for indented-SASS-syntax
files into CSS stylesheets. The full syntax requires `PySCSS`, but a limited syntax
compiles straight to CSS. 

Docs at http://github.com/boscoh/sassin.
"""

setup(
    name='sassin',
    version='0.1',
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/sassin',
    description='compiles indented-SASS-syntax to CSS stylesheets',
    long_description=description,
    license='GPLv3',
    install_requires=['pyscss'],
    py_modules=['sassin',],
    scripts=['sassin'],
)
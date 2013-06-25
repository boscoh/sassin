#!/usr/bin/env python
from setuptools import setup

description = \
"""`sassin` is a Python compiler for indented-SASS-syntax
files fpr CSS stylesheets. The full syntax requires `PySCSS`, but a limited syntax
compiles straight to cSS. Docs at http://github.com/boscoh/indentedsass.
"""

setup(
    name='indentedsass',
    version='0.1',
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/sassin',
    description='Static site generator',
    long_description=description,
    license='GPLv3',
    install_requires=['pyscss'],
    py_modules=['sassin',],
    scripts=['sassin'],
)
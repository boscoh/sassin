#!/usr/bin/env python
from setuptools import setup

setup(
    name='sassin',
    version='0.9.2',
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/sassin',
    description='compiles indented-SASS-syntax to CSS stylesheets',
    long_description="Docs at http://github.com/boscoh/sassin.",
    license='GPLv3',
    install_requires=['pyscss'],
    py_modules=['sassin',],
    scripts=['scripts/sassin'],
)
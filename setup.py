#!/usr/bin/env python
from setuptools import setup

# This is to disable the 'black magic' surrounding versioned repositories... Terrible!
from setuptools.command import sdist
del sdist.finders[:]

description = \
"""IndentedSASS is a Python compiler for SASS indented syntax
file to SCSS. This is a fork of Rapydcss, with
a cleaner API to interact with modules such as HAMLPY.

In the case where no SCSS extensions are used,
it compiles to straight CSS. 

Docs at http://github.com/boscoh/indentedsass.
"""

setup(
    name='indentedsass',
    version='0.1',
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/indentedsass',
    description='Static site generator',
    long_description=description,
    license='GPLv3',
    install_requires=[
        'pyscss',
    ],
    py_modules=['indentedsass',],
    scripts=['sass2css'],
)
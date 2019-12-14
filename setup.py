# -*- coding: utf-8 -*-
"""
setup.py
November 14, 2019
@author Francois Roy
"""
from setuptools import setup


metadata = {}
with open("resources/__init__.py") as fp:
    exec(fp.read(), metadata)


setup(
    name=['__application__'],
    version=metadata['__version__'],
    description=['__short_description__'],
    url='https://github.com/frRoy/cfd',
    author=metadata['__author__'],
    author_email=metadata['__authoremail__'],
    license='MIT',
    packages=['cfd', 'fem', 'gui', 'resources', 'src', 'utils'],
    zip_safe=False
)

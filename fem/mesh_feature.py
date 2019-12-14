# -*- coding: utf-8 -*-
"""
fem.mesh_feature.py
November 14, 2019
@author Francois Roy
"""
from collections import namedtuple
from utils import *
from utils.node import *

CONTAINER = namedtuple('container', ['code', 'label'])


class MeshFeature(Node):
    r"""

     usage:

     .. code-block:: python

          >>> from fem import *

     :param tag: Physics feature tag.
     :type tag: str
     """
    def __init__(self, tag, parent=None, **kwargs):
        super().__init__(tag=tag, parent=parent)
        self._type_info = MESH_FEATURE
        self._valid_children_type = []
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)
        if kwargs.keys():
            for key in kwargs.keys():
                setattr(self, "_"+key, kwargs[key])

    def data(self, column):
        pass

    def set_data(self, column, value):
        pass

# -*- coding: utf-8 -*-
"""
fem.physics.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from utils import *
from utils.node import *


class Physics(Node):
    r"""
    """
    def __init__(self, tag, parent=None):
        super(Physics, self).__init__(tag, parent)
        self._type_info = PHYSICS
        self._valid_children_type = [PHYSICS_FEATURE]
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def component(self):
        r"""Check that the parent is a component."""
        if self._parent is None:
            raise ValueError(error(E_PARENT_NODE_TYPE, None,
                                   self.type_info))
        if not self._parent.type_info == COMPONENT:
            raise ValueError(error(E_PARENT_NODE_TYPE, self._parent.type_info,
                                   self.type_info))
        return self._parent

    def data(self, column):
        pass

    def set_data(self, column, value):
        pass

# -*- coding: utf-8 -*-
"""
fem.study.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from utils import *
from utils.node import *


class Study(Node):
    r"""
    """
    def __init__(self, tag, parent=None, physics_tag=None):
        super(Study, self).__init__(tag, parent)
        self._type_info = STUDY
        self._valid_children_type = [SOLVER_FEATURE]
        self._physics_tag = physics_tag
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def data(self, column):
        pass

    def dataset(self, tag):
        r""""""
        return self.child_by_tag(tag).dataset()

    def set_data(self, column, value):
        pass

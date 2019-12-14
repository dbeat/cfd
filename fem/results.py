# -*- coding: utf-8 -*-
"""
fem.results.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from utils import *
from utils.node import *


class Results(Node):
    r"""
    """

    def __init__(self, tag, parent=None):
        super(Results, self).__init__(tag, parent)
        self._type_info = RESULTS
        self._valid_children_type = [RESULTS_FEATURE]
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def data(self, column):
        pass

    def set_data(self, column, value):
        pass

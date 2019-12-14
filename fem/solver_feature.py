# -*- coding: utf-8 -*-
"""
fem.solver_feature.py
November 14, 2019
@author Francois Roy
"""
from collections import namedtuple
from utils import *
from utils.node import *

CONTAINER = namedtuple('container', ['code', 'label'])


class SolverFeature(Node):
    r"""

     usage:

     .. code-block:: python

          >>> from fem import *

     :param tag: Physics feature tag.
     :type tag: str
     """
    def __init__(self, tag, parent=None, **kwargs):
        super().__init__(tag=tag, parent=parent)
        self._type_info = SOLVER_FEATURE
        self._valid_children_type = [IPCS]
        self._physics = None
        self._mesh = None
        self._solution = None
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)
        if kwargs.keys():
            for key in kwargs.keys():
                setattr(self, "_"+key, kwargs[key])

    def add_physics(self, physics):
        r""""""
        self._physics = physics

    def add_mesh(self, mesh):
        r""""""
        self._mesh = mesh

    def data(self, column):
        pass

    def set_data(self, column, value):
        pass

    @abstractmethod
    def solve(self):
        r""""""
        pass

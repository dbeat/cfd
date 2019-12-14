# -*- coding: utf-8 -*-
"""
fem.geometry_feature.py
November 14, 2019
@author Francois Roy
"""
from collections import namedtuple
from utils import *
from utils.node import *

CONTAINER = namedtuple('container', ['code', 'label'])


class GeometryFeature(Node):
    r"""

     usage:

     .. code-block:: python

          >>> from fem import *

     :param shoe: Add shoe to the core, default = False.
     :type shoe: bool
     """

    def __init__(self, tag, parent=None, origin=(0., 0., 0.), **kwargs):
        super().__init__(tag=tag, parent=parent)
        self._type_info = GEOMETRY_FEATURE
        self._valid_children_type = []
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)
        if kwargs.keys():
            for key in kwargs.keys():
                setattr(self, "_"+key, kwargs[key])
        self._geom_type = None
        self._origin = origin
        self._entities = []
        self._points = None
        self._lines = None
        self._surfaces = None
        self._physical_lines = None
        self._physical_surfaces = None

    def data(self, column):
        pass

    def delete(self):
        r"""Deletes the pygmsh code if exists.

        usage:

         .. code-block:: python

             >>> from copy import deepcopy
             >>> from fem import *
             >>> g = Geometry('g')
             >>> gf = Core('gf', parent=g)
             >>> code = g.gmsh_code()  # gmsh code hasn't been added yet
             >>> len(code)
             2
             >>> gf.run()
             >>> len(code)
             29
             >>> gf.delete()
             >>> len(code)
             2

        :return: None
        """
        if self._parent is None or not self._parent.type_info == GEOMETRY:
            raise ValueError(error(E_PARENT_NODE_TYPE, self._parent))
        g = self._parent
        for e in self._entities:
            # logging.debug("\n{}\n".format(e.code))
            g.gmsh_code().remove(e.code)
            if isinstance(e, CONTAINER):
                if e.label in g.taken_physical_group_ids:
                    g.taken_physical_group_ids().remove(e.label)
        self._entities = []
        # logging.debug("AFTER:\n{}".format(g.gmsh_code()))

    @abstractmethod
    def run(self):
        r"""Generates the pygmsh code for the core."""
        pass

    def get_type(self):
        r"""Get the geometry feature type."""
        return self._geom_type

    def set_data(self, column, value):
        pass

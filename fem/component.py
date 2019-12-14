# -*- coding: utf-8 -*-
"""
fem.component.py
November 14, 2019
@author Francois Roy
"""
from importlib import import_module
from utils.node import *
from resources import *
import fem


class Component(Node):
    r""""""
    def __init__(self, tag, dim, is_axi=False, parent=None):
        super(Component, self).__init__(tag, parent)
        self._dim = dim
        self._is_axi = is_axi
        self._type_info = COMPONENT
        self._valid_children_type = [GEOMETRY, MATERIALS, MESH, PHYSICS]
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def data(self, column):
        pass

    @property
    def dim(self):
        return self._dim

    @property
    def is_axi(self):
        return self._is_axi

    def boundaries(self, tag=None):
        r""""""
        self.check_mesh()
        mesh = self.mesh(tag=tag)
        mvc_bnd = mesh.mvc_bnd()
        return dolfin.cpp.mesh.MeshFunctionSizet(mesh, mvc_bnd)

    def check_mesh(self):
        r"""Check that a mesh exist"""
        if MESH not in [v.type_info for v in self._children]:
            raise (error(E_MESH))

    def subdomains(self, tag=None):
        r""""""
        self.check_mesh()
        mesh = self.mesh(tag=tag)
        mvc_dom = mesh.mvc_dom()
        return dolfin.cpp.mesh.MeshFunctionSizet(mesh, mvc_dom)

    def geometry(self, tag=None):
        r"""Returns the geometry of given tag. If tag is None, returns the
        first geometry in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *
          >>> from fem.geom.block import Block
          >>> m = Model('m')
          >>> c = Component('comp1', 3, m)
          >>> g = Geometry('geom1', c)
          >>> Block('blk1', parent=g)
          >>> g.run()
          >>> c.geometry().tag
          'geom1'

        :param tag: The tag of the geometry instance.
        :type tag: str
        :return: The geometry instance.
        """
        return self.child_by_type(GEOMETRY, tag)

    def material(self, tag=None):
        r"""Returns the material of given tag. If tag is None, returns the
        first material in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *

        :param tag: The tag of the material feature instance.
        :type tag: str
        :return: The material feature instance.
        """
        return self.child_by_type(MATERIALS, tag)

    def mesh(self, tag=None):
        r"""Returns the mesh of given tag. If tag is None, returns the
        first mesh in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *
          >>> from fem.geom.block import Block
          >>> m = Model('m')
          >>> c = Component('comp1', 3, m)
          >>> g = Geometry('geom1', c)
          >>> Block('blk1', parent=g)
          >>> g.run()
          >>> Mesh('mesh1', c, geom_tag=g.tag)
          >>> c.mesh().tag
          'mesh1'

        :param tag: The tag of the mesh instance.
        :type tag: str
        :return: The mesh instance.
        """
        return self.child_by_type(MESH, tag)

    def physics(self, tag=None):
        r""""""
        pass

    def set_data(self, column, value):
        pass

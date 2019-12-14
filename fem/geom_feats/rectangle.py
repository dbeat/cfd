# -*- coding: utf-8 -*-
"""
fem.geom.rectangle.py
November 14, 2019
@author Francois Roy
"""
from fem.geometry_feature import *
from fem.geom_feats.utils import *


class Rectangle(GeometryFeature):
    r"""Creates a rectangle.

    :param tag: The rectangle tag.
    :type tag: str
    :param x0: The 3 first expressions define the lower-left corner.
    :type x0: array-like[3]
    :param a: Rectangle width.
    :type a: float
    :param b: Rectangle height.
    :type b: float
    :param corner_radius: Defines a radius to round the rectangle corners.
    :type corner_radius: float
    :param char_length: Characteristic length of the mesh elements of this
      polygon.
    :type char_length: float
    """
    def __init__(self, tag, x0=(0., 0., 0.), a=Q_(1, 'm'), b=Q_(1, 'm'),
                 corner_radius=None, char_length=None):
        super().__init__(tag, origin=x0)
        self._geom_type = RECTANGLE
        self._x0 = x0
        self._a = a.to('m')
        self._b = b.to('m')
        self._corner_radius = corner_radius
        self._char_length = char_length

    @property
    def a(self):
        r"""The rectangle width."""
        return self._a

    @a.setter
    def a(self, value):
        name = inspect.stack()[0][3]
        value = check_dimension(value, name)
        self._a = value.to('m')

    @property
    def b(self):
        r"""The rectangle height."""
        return self._b

    @b.setter
    def b(self, value):
        name = inspect.stack()[0][3]
        value = check_dimension(value, name)
        self._b = value.to('m')

    @property
    def char_length(self):
        r"""The characteristic length."""
        return self._char_length

    @char_length.setter
    def char_length(self, value):
        name = inspect.stack()[0][3]
        value = check_dimension(value, name)
        self._char_length = value.to('m')

    @property
    def corner_radius(self):
        r"""The corner radius."""
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, value):
        name = inspect.stack()[0][3]
        value = check_dimension(value, name)
        self._corner_radius = value.to('m')

    def run(self):
        r"""Generates the pygmsh code for the rectangle."""
        if self._parent is None or not self._parent.type_info == GEOMETRY:
            raise ValueError(error(E_PARENT_NODE_TYPE, self._parent))
        # make sure to delete previous code feature if exists
        g = self._parent
        self.delete()
        if self._corner_radius:
            # TODO: generate geometry for this option
            raise ValueError(E_NA)
        else:
            self.geometry(g)
        return g.gmsh_code()

    def geometry(self, g):
        r"""Generates gmsh code for the rectangle."""
        if self._char_length:
            l_car = self._char_length.magnitude
        else:
            l_car = None
        x0 = self._x0[0]
        y0 = self._x0[1]
        z0 = self._x0[2]
        a = self._a.magnitude
        b = self._b.magnitude
        # entities
        points = [
            g.add_point(list(self._x0), lcar=l_car),
            g.add_point([x0 + a, y0, z0], lcar=l_car),
            g.add_point([x0 + a, y0 + b, z0], lcar=l_car),
            g.add_point([x0, y0 + b, z0], lcar=l_car),
        ]
        for p in points:
            self._entities.append(p)
        lines = len(points) * [None]
        for i in range(len(points)):
            if i == len(points) - 1:
                lines[i] = g.add_line(points[i], points[0])
            else:
                lines[i] = g.add_line(points[i], points[i + 1])
            self._entities.append(lines[i])
        # create surface
        ll = g.add_line_loop(lines=lines)
        ps = g.add_plane_surface(ll)
        self._entities.append(ll)
        self._entities.append(ps)
        # physical entities --> unique id!!!
        physical_lines = len(lines) * [None]
        for i, l in enumerate(lines):
            physical_lines[i] = g.add_physical(l)
            self._entities.append(physical_lines[i])
        physical_surfaces = [g.add_physical(ps)]
        self._entities.append(physical_surfaces[0])
        self._points = points
        self._lines = lines
        self._surfaces = [ps]
        self._physical_lines = physical_lines
        self._physical_surfaces = physical_surfaces
        return

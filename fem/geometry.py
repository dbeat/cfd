# -*- coding: utf-8 -*-
"""
fem.geometry.py
November 14, 2019
@author Francois Roy
"""
from importlib import import_module
import pygmsh
from collections import namedtuple
from utils import *
from utils.node import *
from resources import GEOMETRY
import fem

CONTAINER = namedtuple('container', ['code', 'label'])


# pygmsh.built_in.geometry
class Geometry(pygmsh.opencascade.Geometry, Node):
    r"""Extends pygmsh.opencascade.Geometry class.
    """
    def __init__(self, tag, parent=None):
        pygmsh.opencascade.Geometry.__init__(self)  # explicit calls
        Node.__init__(self, tag, parent)
        self._type_info = GEOMETRY
        self._valid_children_type = [GEOMETRY_FEATURE]
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def add_physical(self, entities, label=None):
        r"""Makes small changes to the original method.
        The changed method is returning a namedtuple instead of None.
        """
        if not isinstance(entities, list):
            entities = [entities]
        d = {0: "Point", 1: "Line", 2: "Surface", 3: "Volume"}
        tpe = d[entities[0].dimension]
        for e in entities:
            assert isinstance(
                e,
                (
                    pygmsh.built_in.point.Point,
                    pygmsh.built_in.line_base.LineBase,
                    pygmsh.built_in.surface.Surface,
                    pygmsh.built_in.plane_surface.PlaneSurface,
                    pygmsh.built_in.surface_base.SurfaceBase,
                    pygmsh.built_in.volume.Volume,
                    pygmsh.built_in.volume_base.VolumeBase,
                ),
            ), "Can add physical groups only for Points, Lines, Surfaces, " \
               "Volumes, not {}.".format(
                type(e)
            )
            assert d[e.dimension] == tpe
        label = self._new_physical_group(label)
        code = "Physical {}({}) = {{{}}};".format(
                tpe, label, ", ".join([e.id for e in entities]))
        self._GMSH_CODE.append(code)
        return CONTAINER(code=code, label=label)

    def data(self, column):
        pass

    def delete(self):
        r"""Delete all geometry objects."""
        num_children = len(self._children)
        for i in range(num_children):
            self.remove_child(0)
        return True

    def export(self, filename=None):
        r""""""
        name = GEOMETRY
        if filename is None:
            geo_filename = APP_DIR.child(name + '.geo')
        else:
            # check if path exist
            directory = os.path.split(filename)[0]
            if not os.path.exists(filename):
                # check if directory exist and make it if it doesn't
                if not os.path.isdir(directory):
                    os.makedirs(directory)
            geo_filename = filename
        pygmsh.generate_mesh(self, geo_filename=geo_filename)

    def gmsh_code(self):
        r"""Returns GMSH_CODE."""
        return self._GMSH_CODE

    def import_geometry(self, filename):
        r"""Import .geom file"""
        raise ValueError(E_NA)
        # check if path exist
        if not os.path.exists(filename):
            raise ValueError(error(E_PATH, filename))
        self.delete()
        with open(filename, 'r') as f:
            code = f.read()
        # TODO: parse the file and create the children

    def remove_child(self, row):
        r"""override method."""
        if row < 0 or row > len(self._children):
            return False
        child = self._children[row]
        child.delete()  # delete gmsh code
        child = self._children.pop(row)
        child._parent = None
        return True

    def run(self):
        r"""generate the gmsh code for the geometry"""
        for c in self._children:
            c.run()

    def set_data(self, column, value):
        pass

    def taken_physical_group_ids(self):
        r""""""
        return self._TAKEN_PHYSICALGROUP_IDS

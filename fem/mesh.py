# -*- coding: utf-8 -*-
"""
fem.mesh.py
November 14, 2019
@author Francois Roy
"""
import pygmsh
import meshio
import dolfin
from utils import *
from utils.node import *


class Mesh(dolfin.Mesh, Node):
    r"""Use pygmsh to import mesh in dolfin.
    """
    def __init__(self, tag, parent=None, geom_tag=None):
        dolfin.Mesh.__init__(self)  # explicit calls
        Node.__init__(self, tag, parent)
        self._type_info = MESH
        self._valid_children_type = []
        self._geom_tag = geom_tag
        self._mvc_bnd = None
        self._mvc_dom = None
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    @property
    def geom_tag(self):
        return self._geom_tag

    @geom_tag.setter
    def geom_tag(self, value):
        # returns None if it doesn't exist
        self._geom_tag = self._parent.child_by_type(GEOMETRY, value).tag

    def data(self, column):
        pass

    def export(self, filename=None):
        r"""Save mesh in xdmf format."""
        name = MESH
        if filename is None:
            directory = APP_DIR
            # check if directory exist and make it if it doesn't
            if not os.path.isdir(directory):
                os.makedirs(directory)
        else:
            # check if path exist
            directory, name = os.path.split(filename)
            name = name.split(".")[0]  # remove extension if exists
            if not os.path.exists(filename):
                # check if directory exist and make it if it doesn't
                if not os.path.isdir(directory):
                    os.makedirs(directory)
        msh = self.load_geometry()
        if self._parent.dim == 2:
            msh.points = msh.points[:, :2]  # remove z-values to force 2d
        meshio.write(directory.child(name + XDMF), meshio.Mesh(
            points=msh.points,
            cells={"triangle": msh.cells["triangle"]}))
        meshio.write(directory.child(name + BND_XDMF), meshio.Mesh(
            points=msh.points,
            cells={"line": msh.cells["line"]},
            cell_data={
                "line": {"bnd": msh.cell_data["line"]["gmsh:physical"]}
            }
        ))
        meshio.write(directory.child(name + DOM_XDMF), meshio.Mesh(
            points=msh.points,
            cells={"triangle": msh.cells["triangle"]},
            cell_data={
                "triangle": {"dom": msh.cell_data["triangle"]["gmsh:physical"]}
            }
        ))

    def run(self):
        r"""save mesh in xdmf format and load in dolfin"""
        self.export()  # in APP directory
        self.import_mesh()  # from APP directory
        # save vtk file for display?

    def import_mesh(self, filename=None):
        r"""Load mesh from generated xdmf files."""
        name = MESH
        if filename is None:
            directory = APP_DIR
        else:
            # check if path exist
            if not os.path.exists(filename):
                raise ValueError(error(E_PATH, filename))
            directory, name = os.path.split(filename)
            name = name.split(".")[0]  # remove extension if exists
        try:
            mesh = self
            with dolfin.XDMFFile(
                    directory.child(name + XDMF)) as infile:
                infile.read(mesh)
            mvc_bnd = dolfin.MeshValueCollection("size_t", self, 1)
            with dolfin.XDMFFile(
                    directory.child(name + BND_XDMF)) as infile:
                infile.read(mvc_bnd, "bnd")
            mvc_dom = dolfin.MeshValueCollection("size_t", self, 2)
            with dolfin.XDMFFile(
                    directory.child(name + DOM_XDMF)) as infile:
                infile.read(mvc_dom, "dom")
            self._mvc_bnd = mvc_bnd
            self._mvc_dom = mvc_dom
        except RuntimeError as e:
            logging.error("RunTimeError\n{}\n\n".format(e))

    def load_geometry(self):
        r"""Check that the parent is a component. Then check that the
        component has a defined geometry."""
        tag = self._geom_tag
        if tag is None:
            raise ValueError(error(E_GEOM_TAG))
        if self._parent is None:
            raise ValueError(error(E_PARENT_NODE_TYPE, None,
                                   self.type_info))
        if not self._parent.type_info == COMPONENT:
            raise ValueError(error(E_PARENT_NODE_TYPE, self._parent.type_info,
                                   self.type_info))
        geom = self._parent.child_by_type(GEOMETRY, tag=tag)
        if geom is None:
            raise ValueError(error(E_GEOM))
        geom.run()
        return pygmsh.generate_mesh(geom)

    def mvc_bnd(self):
        r"""Mesh Value Collection"""
        self.run()
        return self._mvc_bnd

    def mvc_dom(self):
        r"""Mesh Value Collection"""
        self.run()
        return self._mvc_dom

    def set_data(self, column, value):
        pass

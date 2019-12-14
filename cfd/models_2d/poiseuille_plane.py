# -*- coding: utf-8 -*-
"""
models_2d.poiseuille_plane.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from scipy.constants import g

from utils import *
from fem.geom_feats.utils import check_dimension
import fem


class PoiseuillePlane(fem.Model):
    r"""

    :param tag: The model name -- default pp
    :param size: The length and height of the channel [length, height],
      --default 100 mm and 20 mm.
    :param mu: Dynamic viscosity -- default 8.548e-4 Pa.s (water 300 K).
    :param rho: Density -- default 996.534 kg/m3 (water 300 K).
    :param pin: Inlet pressure -- default 8 Pa.
    :param pout: Outlet pressure -- default 0 Pa.
    :param ne_x: Number of element along the length of the channel
      -- default 100.
    :param ne_y: Number of element along the height of the channel
      -- default 10.
    """
    def __init__(self, tag='pp', size=Q_(np.asarray([20.0, 100.0]), "mm"),
                 mu=Q_(8.548e-4, 'Pa*s'), rho=Q_(996.534, 'kg/m**3'),
                 pin=Q_(8.0, 'Pa'), pout=Q_(0.0, 'Pa'), ne_x=100, ne_y=10):
        super(PoiseuillePlane, self).__init__(tag)
        self._size = size.to("m")
        self._mu = mu.to("Pa*s")
        self._rho = rho.to("kg/m**3")
        self._pin = pin.to('Pa')
        self._pout = pout.to('Pa')
        self._ne_x = int(ne_x)
        self._ne_y = int(ne_y)
        self.create(COMPONENT, 'comp', dim=2)
        self.create(STUDY, 'std')
        self.create(RESULTS, 'res')

    @property
    def size(self):
        r"""The dimensions of the pipe [radius, height]"""
        return self._size

    @size.setter
    def size(self, value):
        # raise invalid syntax if can't convert to string
        name = inspect.stack()[0][3]
        if len(value) != 2:
            raise ValueError("not a valid number of arguments")
        for i in range(2):
            check_dimension(value, name)
        self._size = value.to('m')

    def axial_line(self):
        r"""Define an axial line on which the solution :math:`p` can be
        mapped (interpolated)."""
        x = self._size[1].magnitude
        return Q_(np.linspace(0, x, self._ne_x + 1), 'm')

    def compute(self, t_end=Q_(10.0, 's'), num_steps=500):
        r"""Compute the finite element problem.

        :param t_end:
        :param num_steps:
        :return:
        """
        dt = t_end.to('s').magnitude / num_steps
        length = self._size[0].magnitude
        height = self._size[1].magnitude
        mu = self._mu.magnitude
        rho = self._rho.magnitude
        pin = self._pin.magnitude
        pout = self._pout.magnitude

        self._generate_geometry()  # creates self._geom
        mesh = self._generate_mesh()
        mat = self.component('comp').create(MATERIALS, 'mat')
        # add water density
        mat.add('water', 'x[0] <= 0.5 + tol', 'density', rho)
        # add dynamic viscosity
        mat.add('water', 'x[0] <= 0.5 + tol', 'dynamic_viscosity', mu)

        # set physics
        phys = self.component('comp').create(PHYSICS, 'cfd')
        # add laminar flow
        lam = phys.create(LAMINAR_FLOW, 'lam')  # fluid props from materials
        # create boundary conditions
        lam.inflow('on_boundary && near(x[0], 0.0, tol)',
                   value=dolfin.Constant(pin))
        lam.outflow('on_boundary && near(x[0], {}, tol)'.format(length),
                    value=dolfin.Constant(pout))
        lam.wall('on_boundary && near(x[1], 0) || near(x[1], {})'.format(
            height),
                  value=dolfin.Constant((0.0, 0.0)))
        solver = self.study('std').create(IPCS, 'ipcs1', dt=dt)
        solver.add_mesh(mesh)
        solver.add_physics(lam)
        # solver.solve()
        # results add solution from study to dataset
        line = self.results('res').create(LINE_PLOT, 'lp1')

    def exact_solution(self):
        r"""This method is used to validate the finite element model.
        """
        pass

    def _generate_geometry(self, tag='r1'):
        r"""Generates a rectangle"""
        # TODO: Enable changing geometry
        if 'geom' in [v.tag for v in self.component('comp').children()]:
            return self.component('comp').child_by_tag('geom')
        geom = self.component('comp').create(GEOMETRY, 'geom')
        geom.create(RECTANGLE, tag=tag, a=self._size[0], b=self._size[1])
        geom.run()
        return geom

    def _generate_mesh(self, tag='mesh'):
        r"""Creates mesh from geometry."""
        # TODO: Update mesh after geometry has changed
        if 'mesh' in [v.tag for v in self.component('comp').children()]:
            return self.component('comp').child_by_tag('mesh')
        geom = self._generate_geometry()
        mesh = self.component('comp').create(MESH, tag=tag, geom_tag=geom.tag)
        mesh.run()
        return mesh

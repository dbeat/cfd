# -*- coding: utf-8 -*-
"""
fem.physics.laminar_flow.py
November 14, 2019
@author Francois Roy
"""
from fem.physics_feature import *
from fem.geom_feats.utils import *


class LaminarFlow(PhysicsFeature):
    r"""Creates a rectangle.

    :param tag: The rectangle tag.
    :type tag: str
    """
    def __init__(self, tag, **kwargs):
        super().__init__(tag, **kwargs)
        self._physics = LAMINAR_FLOW
        self._bcs = {}

    def inflow(self, expression, **kwargs):
        r""""""
        inflow = {'subdomain': dolfin.CompiledSubDomain(expression, tol=1e-14)}
        if 'value' in kwargs.keys():
            inflow['value'] = kwargs['value']
        self._bcs['inflow'] = inflow

    def outflow(self, expression, **kwargs):
        r""""""
        outflow = {'subdomain': dolfin.CompiledSubDomain(expression, tol=1e-14)}
        if 'value' in kwargs.keys():
            outflow['value'] = kwargs['value']
        self._bcs['outflow'] = outflow

    def wall(self, expression, **kwargs):
        r""""""
        wall = {'subdomain': dolfin.CompiledSubDomain(expression, tol=1e-14)}
        if 'value' in kwargs.keys():
            wall['value'] = kwargs['value']
        self._bcs['wall'] = wall

    def fes(self):
        r""""""
        comp = self.component()
        mesh = comp.mesh()
        # TODO: Elements should be defined by the model
        v_space = dolfin.VectorFunctionSpace(mesh, 'P', 2)
        q_space = dolfin.FunctionSpace(mesh, 'P', 1)
        return v_space, q_space

    def initial_conditions(self):
        r""""""
        # TODO: Elements should be defined by the model
        return dolfin.Constant((0., 0.))

    def volumetric_force(self):
        r""""""
        # TODO: external force term should be defined by the model
        # define external force
        f = dolfin.Constant((0., 0.))
        return f

    def fluid_properties(self):
        r""""""
        comp = self.component()
        mat = comp.material()  # get the materials node (fluid properties)
        mu = mat.dynamic_viscosity()
        rho = mat.density()
        return rho, mu

    def boundary_conditions(self):
        r"""Generates boundary conditions"""
        v_space, q_space = self.fes()
        # Define boundary conditions
        comp = self.component()
        boundaries = comp.boundaries()
        boundaries.set_all(0)
        bcp = []
        bcu = []
        for key in self._bcs.keys():
            if key == 'inflow':
                self._bcs[key]['subdomain'].mark(boundaries, 1)
                bcp.append(dolfin.DirichletBC(
                    q_space,
                    self._bcs[key]['value'],
                    self._bcs[key]['subdomain']))
            elif key == 'outflow':
                self._bcs[key]['subdomain'].mark(boundaries, 2)
                bcp.append(dolfin.DirichletBC(
                    q_space,
                    self._bcs[key]['value'],
                    self._bcs[key]['subdomain']))
            elif key == 'wall':
                self._bcs[key]['subdomain'].mark(boundaries, 3)
                bcu.append(dolfin.DirichletBC(
                    v_space,
                    self._bcs[key]['value'],
                    self._bcs[key]['subdomain']))

        return bcu, bcp

    def molecular_stress_tensor(self, u, p):
        r"""Define the molecular stress tensor:

        .. math:: \bar{\pi} = 2\mu\bar{\epsilon}-p\bar{I}

        :param u: The velocity field.
        :param p: The pressure field.
        :return: The molecular stress tensor.
        """
        mu = self._mu.magnitude
        epsilon = LaminarFlow.strain_rate_tensor(u)
        return 2 * mu * epsilon - p * dolfin.Identity(len(u))

    @staticmethod
    def strain_rate_tensor(u):
        r"""Define the symmetric strain-rate tensor

        :param u: The velocity field (2D).
        :return: The strain rate tensor.
        """
        return dolfin.sym(dolfin.nabla_grad(u))

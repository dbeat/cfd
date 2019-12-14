# -*- coding: utf-8 -*-
"""
fem.solvers.ipcs.py
November 14, 2019
@author Francois Roy
"""
from fem.solver_feature import *


class Ipcs(SolverFeature):
    r"""Incremental Pressure Correction Scheme (IPCS)  see
    :cite:`Logg2012` chapter 21 for details of the algorithm.

    If we replace the time derivative with a simple difference quotient in the
    Navier-Stokes equation, we obtain a nonlinear system of equations. This in
    itself is not a problem, but the system has a so-called saddle point
    structure and requires special techniques (special preconditioners and
    iterative methods) to be solved efficiently.

    Instead, we can use a simpler and often very efficient approach, known as
    a splitting method. The idea is to consider the Navier-Stokes and
    continuity equations separately. There exist many splitting strategies for
    the incompressible Navier-Stokes equations. One of the oldest is the
    method proposed by Chorin and Temam, often referred to as Chorin's method.

    Here we use a modified version of Chorin's method, the so-called
    incremental pressure correction scheme (IPCS) due to [1] which gives
    improved accuracy compared to the original scheme at little extra cost.

    The IPCS scheme involves three steps...

    https://bazaar.launchpad.net/~nsbench/nsbench/main/files
    """
    def __init__(self, tag, parent=None, num_steps=101, dt=0.1, **kwargs):
        super().__init__(tag=tag, parent=parent)
        self._valid_children_type = []
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)
        if kwargs.keys():
            for key in kwargs.keys():
                setattr(self, "_"+key, kwargs[key])
        self._solver_type = IPCS
        self._num_steps = num_steps
        self._dt = dt

    def solve(self):
        r""""""
        pc = "ilu"  # pre-conditioner

        # Get problem parameters

        # Define function spaces
        v_space, q_space = self._physics.fes()

        # Get initial and boundary conditions
        u0, p0 = self._physics.initial_conditions()
        bcu, bcp = self._physics.boundary_conditions()

        beta = dolfin.Constant(1)

        # Test and trial functions
        v = dolfin.TestFunction(v_space)
        q = dolfin.TestFunction(q_space)
        u = dolfin.TrialFunction(v_space)
        p = dolfin.TrialFunction(q_space)

        # Functions
        u0 = dolfin.interpolate(u0, v_space)
        u1 = dolfin.Function(v_space)
        p0 = dolfin.interpolate(p0, q_space)
        p1 = dolfin.interpolate(p0, q_space)
        mu, rho = self._physics.fluid_properties()
        k = dolfin.Constant(self._dt)
        f = self._physics.volumetric_force()
        n = dolfin.FacetNormal(self._mesh)
        epsilon = self._physics.strain_rate_tensor
        sigma = self._physics.molecuar_stress_tensor
        dx = dolfin.dx
        ds = dolfin.ds

        # Tentative velocity step
        u_mid = 0.5 * (u0 + u)
        f1 = ((1 / k) * dolfin.inner(v, u - u0) * dx +
              dolfin.inner(v, dolfin.grad(u0) * u0) * dx +
              dolfin.inner(epsilon(v), sigma(u_mid, p0, mu)) * dx +
              dolfin.inner(v, p0 * n) * ds -
              beta * mu * dolfin.inner(dolfin.grad(u_mid).T * n, v) * ds -
              dolfin.inner(v, f) * dx)
        a1 = dolfin.lhs(f1)
        l1 = dolfin.rhs(f1)

        """
        # Pressure correction
        a2 = inner(grad(q), grad(p)) * dx
        L2 = inner(grad(q), grad(p0)) * dx - (1 / k) * q * div(u1) * dx

        # Velocity correction
        a3 = inner(v, u) * dx
        L3 = inner(v, u1) * dx - k * inner(v, grad(p1 - p0)) * dx

        # Assemble matrices
        A1 = assemble(a1)
        A2 = assemble(a2)
        A3 = assemble(a3)

        # Time loop
        self.start_timing()
        for t in t_range:

            # Get boundary conditions
            bcu, bcp = problem.boundary_conditions(V, Q, t)

            # Compute tentative velocity step
            b = assemble(L1)
            [bc.apply(A1, b) for bc in bcu]
            solve(A1, u1.vector(), b, "gmres", "ilu")

            # Pressure correction
            b = assemble(L2)
            if len(bcp) == 0 or is_periodic(bcp): normalize(b)
            [bc.apply(A2, b) for bc in bcp]
            if is_periodic(bcp):
                solve(A2, p1.vector(), b)
            else:
                solve(A2, p1.vector(), b, 'gmres', 'hypre_amg')
            if len(bcp) == 0 or is_periodic(bcp): normalize(p1.vector())

            # Velocity correction
            b = assemble(L3)
            [bc.apply(A3, b) for bc in bcu]
            solve(A3, u1.vector(), b, "gmres", pc)

            # Update
            self.update(problem, t, u1, p1)
            u0.assign(u1)
            p0.assign(p1)
        
        # Time-stepping
        t = 0
        for n in range(self._num_steps):
            # Update current time
            t += self._dt

            # Step 1: Tentative velocity step
            b1 = dolfin.assemble(L1)
            [bc.apply(b1) for bc in bcu]
            dolfin.solve(A1, u_.vector(), b1)

            # Step 2: Pressure correction step
            b2 = dolfin.assemble(L2)
            [bc.apply(b2) for bc in bcp]
            dolfin.solve(A2, p_.vector(), b2)

            # Step 3: Velocity correction step
            b3 = dolfin.assemble(L3)
            dolfin.solve(A3, u_.vector(), b3)

            # Update previous solution
            u_n.assign(u_)
            p_n.assign(p_)
        self._solution = u_n, p_n
        return u_n, p_n
        """
        return None


# -*- coding: utf-8 -*-
"""
tests.models_2d.test_poiseuille_plane.py
November 14, 2019
@author Indigo Technologies Inc.
"""
import pytest
from cfd.models_2d.poiseuille_plane import *

TEST_DIR = Path(os.path.abspath(__file__)).ancestor(1)
REF_DIR = TEST_DIR.child("references")


@pytest.mark.skip("This test should be somewhere else")
class TestPoiseuillePlane:
    r""""""
    def test_geom(self, fix):
        r"""Test the area of the rectangular geometry using numerical
        integration.

        :param fix: The fixture --see
          :func:`fix<tests.cfd.models_2d.conftest.fix>`
        """
        p_plane = fix.object.get('p_plane')
        mesh = p_plane.mesh
        dom = dolfin.cpp.mesh.MeshFunctionSizet(mesh, mesh.mvc_dom())
        dx = dolfin.Measure("dx", domain=mesh, subdomain_data=dom)
        size = p_plane.size
        desired = (size[0] * size[1]).magnitude
        actual = dolfin.assemble(dolfin.Constant(1.) * dx)
        np.testing.assert_almost_equal(actual, desired, 7, 'error', True)

    @pytest.mark.skip("This test should be somewhere else")
    def test_strain_rate_tensor(self, fix):
        r"""Test the strain-rate tensor using an engineered velocity field:

        .. math:: \mathbf{u} = (2x^2 - 4y) \mathbf{\hat{e}}_x +
                              (-4x^3 + 3y^2 - 6y) \mathbf{\hat{e}}_y

        which gives the following tensor components:

        .. math:: \epsilon[0,0] &= 4x\\
                  \epsilon[0,1] &= \epsilon[1,0] = -(12x^2+4)/2\\
                  \epsilon[1,1] &= 6y - 6

        :param fix: The fixture --see
          :func:`fix<tests.cfd.models_2d.conftest.fix>`
        """
        p_plane = fix.object.get('p_plane')
        mesh = p_plane.mesh
        # define a vector function space for the velocity field
        fes = dolfin.VectorFunctionSpace(mesh, 'P', 2)
        expr = dolfin.Expression((
            "2*x[0]*x[0]-4*x[1]",
            "-4*pow(x[0], 3)+3*x[1]*x[1]-6*x[1]"), degree=2)
        u = dolfin.interpolate(expr, fes)
        epsilon = PoiseuillePlane.strain_rate_tensor(u)
        # define another function space for the strain rate tensor evaluation
        t_space = dolfin.TensorFunctionSpace(mesh, 'CG', 1)
        epsilon = dolfin.project(epsilon, t_space)
        actual = []
        desired = []
        for i in range(2):
            for j in range(2):
                for c in mesh.coordinates():
                    actual.append(epsilon[i, j](c))
                    if i == 0 and j == 0:  # epsilon[0, 0]
                        desired.append(4 * c[0])
                    elif i == 1 and j == 1:  # epsilon[1, 1]
                        desired.append(6 * c[1] - 6.)
                    else:  # off diagonal terms
                        desired.append(0.5 * (-4. - 12. * c[0]**2))
        np.testing.assert_almost_equal(actual, desired, 4, 'error', True)

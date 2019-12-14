# -*- coding: utf-8 -*-
"""
tests.models_2d.axi_symmetric.test_poiseuille_axi.py
November 14, 2019
@author Indigo Technologies Inc.
"""
import pytest
from cfd.models_2d.axi_symmetric.poiseuille_axi import *

TEST_DIR = Path(os.path.abspath(__file__)).ancestor(1)
REF_DIR = TEST_DIR.child("references")


# @pytest.mark.skip("skipped for now")
class TestPoiseuilleAxi:
    r""""""
    def test_geom(self, fix):
        r"""Test the area of the axisymmetric geometry using numerical
        integration.

        :param fix: The fixture --see
          :func:`fix<tests.cfd.models_2d.axi_symmetric.conftest.fix>`
        """
        p_axi = fix.object.get('p_axi')
        size = p_axi.size
        desired = (size[0] * size[1]).magnitude
        mesh = p_axi._mesh
        dom = dolfin.cpp.mesh.MeshFunctionSizet(mesh, mesh.mvc_dom())
        dx = dolfin.Measure("dx", domain=mesh, subdomain_data=dom)
        actual = dolfin.assemble(dolfin.Constant(1.) * dx)
        np.testing.assert_almost_equal(actual, desired, 7, 'error', True)

    def test_strain_rate_tensor(self, fix):
        r"""

        :param fix: The fixture --see
          :func:`fix<tests.cfd.models_2d.axi_symmetric.conftest.fix>`
        """
        p_axi = fix.object.get('p_axi')
        mesh = p_axi._mesh

        # define a finite element space
        fes = dolfin.VectorFunctionSpace(mesh, 'CG', degree=2)
        u = dolfin.TrialFunction(fes)
        epsilon = p_axi.strain_rate_tensor(u)
        # project inner(epsilon, epsilon) on the finite element space
        # a = dolfin.project(dolfin.inner(epsilon, epsilon), fes)
        # a = dolfin.interpolate(epsilon, fes)
        # Dump solution to file in VTK format
        # file = dolfin.File(OUT_DIR.child("a.pvd"))
        # file << a
        # actual = 1.
        # desired = 2.
        # np.testing.assert_almost_equal(actual, desired, 7, 'error', True)

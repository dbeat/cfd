# -*- coding: utf-8 -*-
"""
tests.fem.test_geometry.py
November 14, 2019
@author Francois Roy
"""
import pytest
from utils import *


TEST_DIR = Path(os.path.abspath(__file__)).ancestor(1)
DATA_DIR = TEST_DIR.child("data")


class TestGeometry:
    def test_create(self, fix):
        """
        :param fix: The fixture --see :func:`fix<tests.fem.conftest.fix>`
        """
        m = fix.object.get('m')
        c = m.create(COMPONENT, 'comp', dim=2)
        geom = c.create(GEOMETRY, 'geom')
        size = Q_(np.asarray([20.0, 100.0]), "mm")
        geom.create(RECTANGLE, tag='r1', a=size[0], b=size[1])
        geom.run()
        mesh = c.create(MESH, tag='mesh', geom_tag=geom.tag)
        mesh.run()
        actual = ""
        desired = ""
        np.testing.assert_string_equal(actual, desired)
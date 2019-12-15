# -*- coding: utf-8 -*-
"""
tests.fem.conftest.py
November 14, 2019
@author Francois Roy
"""
import pytest
from collections import namedtuple

import dolfin
# from utils import *
# from fem.geom_feats.utils import check_dimension
# import fem

Container = namedtuple('Container', ['object'])


@pytest.fixture()
def fix():
    r"""The default fixture to test the fem package.

    :return: The fixture for fem tests.
      (:func:`Container<tests.fem.conftest.Container>`)
    """
    # m = fem.Model('m')
    m = dolfin.__version__
    return Container({'m': m})

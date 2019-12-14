# -*- coding: utf-8 -*-
"""
tests.cfd.models_2d.axi_symmetric.conftest.py
November 14, 2019
@author Indigo Technologies Inc.
"""
import pytest
from collections import namedtuple

from cfd.models_2d.axi_symmetric.poiseuille_axi import *


Container = namedtuple('Container', ['object'])


@pytest.fixture()
def fix():
    r"""The fixture for testing the two-dimensional models.

    :return: The fixture for two-dimensional models.
      (:func:`Container<tests.models_2d.axi_symmetric.conftest.Container>`)
    """
    p_axi = PoiseuilleAxi()

    return Container({
        'p_axi': p_axi,
    })

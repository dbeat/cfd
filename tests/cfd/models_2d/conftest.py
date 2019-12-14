# -*- coding: utf-8 -*-
"""
tests.cfd.models_2d.conftest.py
November 14, 2019
@author Indigo Technologies Inc.
"""
import pytest
from collections import namedtuple

from cfd.models_2d.poiseuille_plane import *


Container = namedtuple('Container', ['object'])


@pytest.fixture()
def fix():
    r"""The fixture for testing the two-dimensional models.

    :return: The fixture for two-dimensional models.
      (:func:`Container<tests.models_2d.conftest.Container>`)
    """
    p_plane = PoiseuillePlane()

    return Container({
        'p_plane': p_plane,
    })

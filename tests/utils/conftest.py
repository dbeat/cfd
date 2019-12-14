# -*- coding: utf-8 -*-
"""
tests.utils.conftest.py
November 14, 2019
@author Francois Roy
"""
import pytest
from collections import namedtuple

Container = namedtuple('Container', ['object'])


@pytest.fixture()
def fix():
    r"""The fixture for testing the tree structure.

    :return: The fixture for tree structure tests.
      (:func:`Container<tests.utils.conftest.Container>`)
    """
    return Container({'m': {}})

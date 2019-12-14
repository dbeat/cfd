# -*- coding: utf-8 -*-
"""
tests.utils.test_util.py
November 14, 2019
@author Francois Roy
"""
import pytest
from utils import *


TEST_DIR = Path(os.path.abspath(__file__)).ancestor(1)
DATA_DIR = TEST_DIR.child("data")


class TestUtil:
    def test_load(self, fix):
        """
        :param fix: The fixture --see :func:`fix<tests.utils.conftest.fix>`
        """
        # create model
        model = fix.object.get('m')
        actual = ""
        desired = ""
        np.testing.assert_string_equal(actual, desired)

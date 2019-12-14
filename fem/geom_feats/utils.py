# -*- coding: utf-8 -*-
"""
fem.geom.utils.py
November 14, 2019
@author Francois Roy
"""
from utils import *


def check_dimension(value, name, dim='[length]'):
    r"""

    :param value: The value to be checked.
    :param name: The name of the property.
    :param dim: The dimensionality of the unit.
    :return:
    """
    if isinstance(value, str):
        value = Q_(value)
    if not value.check(dim):
        raise ValueError(error(E_QTY, str(value.dimensionality), dim))
    if value.magnitude <= 0:
        raise ValueError(error(E_VALID, value, name))
    return value

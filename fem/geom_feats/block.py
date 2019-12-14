# -*- coding: utf-8 -*-
"""
fem.geom.block.py
November 14, 2019
@author Francois Roy
"""
from fem.geometry_feature import *


class Block(GeometryFeature):
    r""""""
    def __init__(self, tag, x0=(0., 0., 0.), a=Q_(1, 'm'), b=Q_(1, 'm'),
                 corner_radius=None, char_length=None):
        super(Block, self).__init__(tag, origin=x0)
        self._x0 = x0
        self._a = a.to('m')
        self._b = b.to('m')
        self._corner_radius = corner_radius
        self._char_length = char_length

    def run(self):
        pass

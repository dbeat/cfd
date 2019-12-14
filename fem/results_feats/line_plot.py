# -*- coding: utf-8 -*-
"""
fem.results_feats.line_plot.py
November 14, 2019
@author Francois Roy
"""
from fem.results_feature import *


class LinePlot(ResultsFeature):
    r"""
    """
    def __init__(self, tag, parent=None, **kwargs):
        super().__init__(tag=tag, parent=parent)
        self._valid_children_type = []
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)
        if kwargs.keys():
            for key in kwargs.keys():
                setattr(self, "_"+key, kwargs[key])
        self._results_type = LINE_PLOT
        self._line = None

    def line(self, line):
        r"""line over which data are evaluated."""
        self._line = line

    def plot(self):
        r""""""
        pass

# -*- coding: utf-8 -*-
"""
gui.views.central_view.py
October 10, 2019
@author: Francois Roy

This file contains the main central view widget and the component editors.
The measurement view is written in a separate file for clarity.
"""
from PyQt5 import uic
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFormLayout
from utils import ROOT_DIR


VIEWS_DIR = ROOT_DIR.child('gui').child('views')

BASE, FORM = uic.loadUiType(VIEWS_DIR.child('central.ui'))


class CentralView(BASE, FORM):
    r"""The central widget."""
    def __init__(self, parent=None):
        super(BASE, self).__init__(parent)
        self.setupUi(self)
        self.app = parent  # the app
        self._model = None

        settings_layout = QFormLayout()
        self.frame.setLayout(settings_layout)

        # initialize views
        # self._measurement_view = MeasurementView(parent)
        # settings_layout.addWidget(self._measurement_view)

        # set initial visibility
        # self._measurement_view.setVisible(True)

    def set_model(self, model):
        r"""Maps user inputs to model.

        :param model: The model instance.
        """
        pass
        # self._model = model
        # self._measurement_view.set_model(model)

    def set_selection(self, current):
        """Sets the current tree selection visible.

        :param current: The current selection.
        :type current: QModelIndex
        """
        node = current.internalPointer()
        if node is not None:
            type_info = node.type_info

            # set visibility for the current view
            """
            if type_info == MEASUREMENT:
                self._measurement_view.setVisible(True)
                self._measurement_view.set_selection(current)
            else:
                self._measurement_view.setVisible(False)
            """

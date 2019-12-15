# gui/tree_view.py
# Nucleus Scientific Inc.
# December 18, 2017
from PyQt5.QtCore import Qt, QItemSelectionModel, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QMenu, QDataWidgetMapper, QMessageBox)
from PyQt5 import uic
from .. import *

from utils import ROOT_DIR
VIEW_DIR = ROOT_DIR.child('gui').child('views')

base_tree, form_tree = uic.loadUiType(VIEW_DIR.child('tree.ui'))


class TreeView(base_tree, form_tree):
    """

    """
    def __init__(self, model):
        super(base_tree, self).__init__()
        self.setupUi(self)
        self._model = model
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_menu)
        # assign model to view
        self.tree_view.setModel(model)

    def delete_element(self, index):
        """

        :param index:
        :return:
        """
        pass

    def remove_result_node(self, index):
        """

        :param index:
        :return:
        """
        pass

    def open_menu(self, position):
        indexes = self.tree_view.selectedIndexes()


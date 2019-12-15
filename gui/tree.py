# -*- coding: utf-8 -*-
"""
gui.tree.py
July 16, 2019
@author: Francois Roy
"""
from importlib import import_module
from PyQt5.QtCore import (QAbstractItemModel, QStringListModel,
                          Qt, QVariant, QModelIndex)
from PyQt5.QtGui import QIcon
import threading
from fem import *
from resources import *
from copy import deepcopy

EXTRA = {'qthreadName': threading.current_thread().name}


class Tree(QAbstractItemModel):
    r"""The tree model.

    The root item (empty) in the tree structure has no parent item and it is
    never referenced outside the model.
    """
    def __init__(self, name, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.extra = {'qthreadName': threading.current_thread().name}
        self._name = name
        # initialize fixed tree elements
        self._root = Model('model')

    def columnCount(self, parent=QModelIndex(), *args, **kwargs):
        """The number of entries (columns) is fixed to 20 for all nodes.

        :param parent: The index of the node.
        :type parent: QModelIndex
        :return: The number of entries for the node (int).
        """
        return 20

    def data(self, index, role=None):
        """

        :param index:
        :type index: QModelIndex
        :param role:
        :type role: int
        :return:
        """
        if not index.isValid():
            return None

        node = self.get_node(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return node.data(index.column())
            # return node.name

        if role == Qt.DecorationRole:
            # the icon is a position 0 for all nodes
            if index.column() == 0:
                return QIcon(node.resource())

    def flags(self, index):
        """

        :param index:
        :type index: QModelIndex
        :return:
        """
        node = self.get_node(index)
        type_info = node.type_info

        if type_info is None:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def get_node(self, index):
        """

        :param index:
        :type index: QModelIndex
        :return:
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._root

    def index(self, row, column, parent=QModelIndex(), *args, **kwargs):
        """
        Return the child index at a given row, given column and given parent.

        :param row:
        :type row: int
        :param column:
        :type column: int
        :param parent:
        :type parent: QModelIndex
        :param args:
        :param kwargs:
        :return:
        """
        if self.hasIndex(row, column, parent):
            parent_node = self.get_node(parent)

            child_item = parent_node.child(row)
            if child_item:
                return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def insertRows(self, row, count, parent=QModelIndex(), *args, **kwargs):
        """
        :param row: Index of the child in the parent's children list. Her it is
          always 0, i.e. the child is prepend to the existing children list.
        :type row: int
        :param count: The number of children to insert in the parent's children
          list. Here is is always 1.
        :type count: int
        :param parent: The index of the parent.
        :type parent: QModelIndex
        :return: True if the rows were successfully inserted; otherwise returns
          False.
        """
        return True

    def headerData(self, section, orientation, role=None):
        """

        :param section:
        :type section: int
        :param orientation:
        :type orientation: int
        :param role:
        :type role: int
        :return:
        """
        if role == Qt.DisplayRole:
            if section == 0:
                return "Measurement header"

    def parent(self, index=None):
        """
        Return the parent of the node of given index.

        :param index:
        :type index: QModelIndex
        :return: The parent of the node (QModelIndex).
        """
        node = self.get_node(index)
        parent_node = node.parent()

        if parent_node == self._root:
            # returns an empty QModelIndex (root has no parents)
            return QModelIndex()
        # create index
        return self.createIndex(parent_node.row(), 0, parent_node)

    def removeRows(self, position, rows, parent=QModelIndex(), **kwargs):
        """

        :param position:
        :type position: int
        :param rows:
        :type rows: int
        :param parent:
        :type parent: QModelIndex
        :return:
        """
        parent_node = self.get_node(parent)
        node = parent_node.child(position)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parent_node.remove_child(position)
        self.endRemoveRows()
        return success

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        """Get the number of children of a given node.

        :param parent: The parent index.
        :type parent: QModelIndex
        :param args:
        :param kwargs:
        :return:
        """
        if not parent.isValid():
            parent_node = self._root
        else:
            parent_node = parent.internalPointer()
        return len(parent_node.children())

    def setData(self, index, value, role=Qt.EditRole):
        """

        :param index:
        :type index: QModelIndex
        :param value:
        :type value: QVariant
        :param role:
        :type role: int
        :return:
        """
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.EditRole:
                try:
                    node.set_data(index.column(), value)
                except (ValueError, RuntimeError) as exception:
                    logging.error(str(exception), extra=EXTRA)
                # signal form the inherited class
                self.dataChanged.emit(index, index)
                return True
        return False

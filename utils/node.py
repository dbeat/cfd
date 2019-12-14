# -*- coding: utf-8 -*-
"""
utils.node.py
November 14, 2019
@author Francois Roy
"""
from importlib import import_module
from enum import Enum
from . import ureg, Path, os, np, logging, Q_
from resources import *
from abc import abstractmethod
import dolfin


class JSONWriter:
    r"""Write abstract data to a JSON file."""
    def __init__(self, root):
        self._root = root

    def as_json(self, parent):
        r"""Use recursion to write the file."""
        doc = {'attributes': parent.attributes(), 'children': []}
        for child in parent.children():
            doc['children'].append(self.as_json(child))
        return doc

    def get_data(self):
        r""""""
        return self.as_json(self._root)


class Node(object):
    r"""A tree data structure can be defined recursively as a collection of
    nodes (starting at a root node), where each node is a data structure
    consisting of a value, together with a list of references to nodes
    (the "children"), with the constraints that no reference is duplicated,
    and None points to the root.

    :param tag: The name of the node.
    :type tag: str
    :param parent: The parent node, None if not provided.
    :type parent: Node
    """
    def __init__(self, tag, parent=None):
        self._tag = tag
        self._type_info = NODE
        self._parent = parent
        self._valid_children_type = None
        self._children = []

    def __repr__(self):
        return self._tag

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        # raise invalid syntax if can't convert to string
        self._tag = str(value)

    @property
    def type_info(self):
        return self._type_info

    def attributes(self):
        r"""Returns the node attributes, for instance:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n = Node("my_node")
          >>> n.attributes()
          {'name': 'my_node', 'type_info': 'node'}

        :return: A dictionary containing the node attributes.
        """
        # mro() stands for Method Resolution Order. It returns a list of
        # types the class is derived from, in the order they are searched
        # for methods.
        classes = self.__class__.mro()
        # classes = [ <class 'abstract.node.Node'>, <class 'object'>]
        kv = {}
        for cls in classes:
            for k, v in cls.__dict__.items():
                if isinstance(v, property):
                    # remove inherited properties
                    if not isinstance(v.fget(self),
                                      dolfin.cpp.parameter.Parameters):
                        kv[k] = v.fget(self)
                        if isinstance(kv[k], ureg.Quantity):
                            kv[k] = str(kv[k])
                        if isinstance(kv[k], Enum):
                            kv[k] = kv[k].tag
                        if kv[k] is None:
                            kv[k] = 'None'
        return kv

    def add_child(self, child):
        r"""Adds child node to the children list.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n1.add_child(n2)
          >>> n1.child(0).tag
          'my_node_2'

        :param child: A node instance.
        :type child: Node
        """
        # TODO: make sure the name of the child is not used
        self.check_child(child)
        self.check_tag(child.tag)
        self._children.append(child)
        child._parent = self

    def check_child(self, child):
        r"""Check if the child has a valid type for the parent.

        :param child:
        :return: None
        """
        if self._valid_children_type is not None:
            if child.type_info not in self._valid_children_type:
                parent_type = None
                if self._type_info is not None:
                    parent_type = self._type_info
                raise ValueError(error(E_CHILD_NODE_TYPE, child.type_info,
                                       parent_type))
        return

    def check_tag(self, tag):
        r"""Make sure the tag is not used by the parent or a sibling.

        :param tag: The tag to be checked.
        :type tag: str
        return: True if the tag is valid.
        """
        if (tag in [child.tag for child in self._children] or
                tag == self._tag):
            raise ValueError('not a valid tag, used elsewhere')
        return True

    def child(self, index):
        r"""Returns the node in the children list at the position index.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n1.add_child(n2)
          >>> n1.child(0).tag
          'my_node_2'

        :param index: The index.
        :type index: int
        :return: The node of the children at the position index.
        """
        return self._children[index]

    def child_by_tag(self, tag):
        r"""Returns the node in the children list of a given tag.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n1.add_child(n2)
          >>> n1.child_by_tag("my_node_2").tag
          'my_node_2'

        :param tag: The tag.
        :type tag: str
        :return: The node of the children at the position index.
        """
        children_tags = [t.tag for t in self._children]
        if tag not in children_tags:
            raise ValueError(error(E_TAG, tag, self._tag))
        return self._children[children_tags.index(tag)]

    def child_by_type(self, type_info, tag=None):
        r"""Returns the child of a given type and tag. If tag is None,
        returns the first child that match the type in the list of children.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n1.add_child(n2)
          >>> n1.child_by_type("node").tag
          'my_node_1'
          >>> n1.child_by_type("node", "my_node_2").tag
          'my_node_2'

        :param type_info: The type_info.
        :type type_info: str
        :param tag: The tag.
        :type tag: str
        :return: The node of the children at the position index.
        """
        children_types = [t.type_info for t in self._children]
        if type_info in children_types:
            tags = [t.tag for t in self._children]
            if tag in tags:
                return self._children[tags.index(tag)]
            else:  # return the first component of the list
                return self._children[children_types.index(type_info)]

    def children(self):
        r"""Returns list of children nodes.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n3 = Node("my_node_3")
          >>> n1.add_child(n2)
          >>> n1.add_child(n3)
          >>> n1.children
          ['my_node_2', 'my_node_3']

        :return: The children list of nodes.
        """
        return self._children

    def create(self, type_info, tag, **kwargs):
        r"""Create and add a valid child to the node. If
        ``valid_children_type`` is None, the method returns None.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n1.create('geometry', 'geom')
          None

        :param type_info: The type info of the child.
        :param tag: The tag of the child.
        :param kwargs: Extra arguments.
        :return: The feature instance or None if not a valid child.
        """
        type_info = type_info.lower().capitalize()  # lower then capitalize
        if "_" in type_info:
            ind = type_info.index("_")
            type_info = (type_info[:ind+1] + type_info[ind+1].swapcase() +
                         type_info[ind+2:])
            type_info = type_info.replace("_", "")
        try:
            cls = getattr(import_module('fem'), type_info)
            feature = cls(tag, **kwargs)
            self.add_child(feature)
        except(AttributeError, ValueError) as e:
            logging.error(error(E_CREATE, e))
            feature = None
        return feature

    @abstractmethod
    def data(self, column):
        r"""Returns the attribute of the node corresponding to the column
        number. The data for a parent node are organized as follow:

        .. _data_structure:
        .. csv-table:: Data Structure
            :header: "", "dat0", "dat1", "...", "datn"
            :widths: 2, 2, 2, 2, 2

            "child0", "", "", "", ""
            "child1", "", "", "", ""
            ":math:`\vdots`", "", "", "", ""
            "childn", "", "", "", ""

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n = Node("my_node")
          >>> n.data(0)
          'my_node'

        :param column: The index of the column where the data is stored.
        :type column: int
        :return: The data at the given position.
        """
        if column == 0:
            return self._tag

    def insert_child(self, row, child):
        r"""Inserts a child node in the children list at the given position.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n3 = Node("my_node_3")
          >>> n4 = Node("my_node_4")
          >>> n1.add_child(n2)
          >>> n1.add_child(n3)
          >>> n1.insert_child(1, n4)
          True
          >>> n1.children
          ['my_node_2', 'my_node_4', 'my_node_3']

        :param row: The position in the list.
        :type row: int
        :param child: The child node.
        :type child: Node
        :return: True if the operation succeeded.
        """
        if row < 0 or row > len(self._children):
            return False
        # TODO: make sure the name of the child is not used
        self.check_child(child)
        self.check_tag(child.tag)
        self._children.insert(row, child)
        child._parent = self
        return True

    def parent(self):
        r"""return the parent of the instance.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n1.add_child(n2)
          >>> n2.parent()
          'my_node_1'

        :return: The parent of the node instance.
        """
        return self._parent

    def row(self):
        r"""Returns the index of the child relative to its parent if not None.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n3 = Node("my_node_3")
          >>> n1.add_child(n2)
          >>> n1.add_child(n3)
          >>> n3.row()
          1

        :return: The position of the node in the parent's children list.
        """
        if self._parent is not None:
            return self._parent.children().index(self)

    def remove_child(self, row):
        r"""Removes the child at the given position in the children list.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n3 = Node("my_node_3")
          >>> n4 = Node("my_node_4")
          >>> n1.add_child(n2)
          >>> n1.add_child(n3)
          >>> n1.insert_child(1, n4)
          True
          >>> n1.children
          ['my_node_2', 'my_node_4', 'my_node_3']
          >>> n1.remove_child(1)
          ['my_node_2', 'my_node_3']

        :param row: The position of the child in the list.
        :type row: int
        :return: True if the operation succeeded.
        """
        if row < 0 or row > len(self._children):
            return False
        child = self._children.pop(row)
        child._parent = None
        return True

    def set_attributes(self, kv):
        r"""Set attributes from a dictionary.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n = Node("my_node")
          >>> kv = n.attributes()
          >>> n1 = Node("new_node")
          >>> n1.attributes()
          {'tag': 'new_node', 'type_info': 'node'}
          >>> n1.set_attributes(kv)
          >>> n1.attributes()
          {'tag': 'my_node', 'type_info': 'node'}

        :param kv: The dictionary.
        :type kv: dict
        """
        classes = self.__class__.mro()
        # classes = [ <class 'abstract.node.Node'>, <class 'object'>]
        for cls in classes:
            for k, v in cls.__dict__.items():
                if isinstance(v, property):
                    if k in kv.keys() and k != 'type_info' and k != 'dim':
                        v.fset(self, kv[k])

    @abstractmethod
    def set_data(self, column, value):
        r"""Assigns a specific attribute of the node to the column number
        -- see :ref:`data_structure`.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n = Node("my_node")
          >>> n.set_data(0, "my_renamed_node")
          >>> n.tag
          'my_renamed_node'

        :param column: The column index.
        :type column: int
        :param value: The value of the attribute.
        :type value: object
        """
        if column == 0:
            self._tag = value

    def type_count(self, type_info):
        r"""Returns the number of child having the same type_info.

        Example:

        .. code-block:: python

          >>> from utils.node import Node
          >>> n1 = Node("my_node_1")
          >>> n2 = Node("my_node_2")
          >>> n3 = Node("my_node_3")
          >>> n1.add_child(n2)
          >>> n1.add_child(n3)
          >>> ni.type_count('node')
          '2'

        :param type_info: The type of node.
        :type type_info: str
        :return: The number of children with the same type_info.
        """
        children_type = [t.type_info for t in self._children]
        return children_type.count(type_info)

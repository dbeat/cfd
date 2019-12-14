# -*- coding: utf-8 -*-
"""
fem.model.py
November 14, 2019
@author Francois Roy
"""
from utils import *
import pathlib
from importlib import import_module
from utils.node import *
import json
from zipfile import ZipFile
from resources import *
from fem import (Component, Study, Results, Geometry, Mesh, Physics,
                 Materials)


class Model(Node):
    r"""The model node is the root and has no parent.

    """
    def __init__(self, tag):
        super().__init__(tag)
        self._type_info = MODEL
        self._valid_children_type = [COMPONENT, RESULTS, STUDY]

    def component(self, tag=None):
        r"""Returns the component of given tag. If tag is None, returns the
        first component in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *
          >>> m = Model('my_model')
          >>> c1 = Component("my_component_1", dim=2)
          >>> c2 = Component("my_component_2", dim=3)
          >>> m.component()  # first of the list
          'my_component_1'
          >>> m.component('my_component_2')
          'my_component_2'

        :param tag: The tag of the component instance.
        :type tag: str
        :return: The component instance.
        """
        return self.child_by_type(COMPONENT, tag)

    @abstractmethod
    def compute(self):
        r""""""
        pass

    def data(self, column):
        pass

    def generate_model(self, data, parent):
        r"""Use recursion to generate the model.

        :param data:
        :type data:
        :param parent:
        :type parent:
        :return:
        """
        if parent.type_info == MESH:
            print(parent.attributes())
        parent.set_attributes(data['attributes'])
        if parent.type_info == MESH:
            print(parent.attributes())
        for child in data['children']:
            tag = child.get('attributes')['tag']
            type_info = child.get('attributes')['type_info']
            if type_info == COMPONENT:
                dim = child.get('attributes')['dim']
                c = Component(tag, dim, parent=parent)
            elif type_info == GEOMETRY_FEATURE:
                geom_type = child.get('attributes')['geom_type']
                cls = getattr(import_module('cfd'), type_info.capitalize())
                c = cls(tag, parent=parent)
            else:
                cls = getattr(import_module('fem'), type_info.capitalize())
                c = cls(tag, parent=parent)
            self.generate_model(child, c)

    def results(self, tag=None):
        r"""Returns the results node of a given tag. If tag is None, returns
        the first results node in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *
          >>> m = Model('my_model')
          >>> res1 = Study("res1")
          >>> res2 = Study("res2")
          >>> m.results()  # first of the list
          'res1'
          >>> m.results('res2')
          'res2'

        :param tag: The tag of the results instance.
        :type tag: str
        :return: The results instance.
        """
        return self.child_by_type(RESULTS, tag)

    def save(self, filename, file_type='igo'):
        r"""Save the model, save to current directory if no valid path
        provided.

        Example:

        .. code-block:: python

          >>> import os
          >>> from fem.model import Model
          >>> from unipath import Path
          >>> DIR = Path(os.getcwd())
          >>> model = Model("my_model")
          >>> model.save(DIR.child('my_file'), "igo")

        :param filename:
        :param file_type:
        :return: The data in JSON format.
        """
        # TODO: override?
        name = filename.split("/")[-1]
        if not os.path.isdir(filename.strip(name)):
            filename = Path(os.getcwd()).child(name)
        writer = JSONWriter(self)
        data = writer.get_data()
        json_data = json.dumps(data, sort_keys=True, indent=4)
        with ZipFile(filename + "." + file_type, 'w') as f:
            f.writestr('digest.json', json_data)
            # add other files?
            # f.write(APP_DIR.child('mesh.h5'))
        return json_data

    def set_data(self, column, value):
        pass

    def study(self, tag=None):
        r"""Returns the study of given tag. If tag is None, returns the
        first component in the list of children.

        example:

        .. code-block:: python

          >>> from fem import *
          >>> m = Model('my_model')
          >>> s1 = Study("std11")
          >>> s2 = Study("std2")
          >>> m.study()  # first of the list
          'std1'
          >>> m.study('std2')
          'std2'

        :param tag: The tag of the study instance.
        :type tag: str
        :return: The study instance.
        """
        return self.child_by_type(STUDY, tag)

# -*- coding: utf-8 -*-
"""
utils.util.py
November 14, 2019
@author Francois Roy
"""
import os
import json
from zipfile import ZipFile
from unipath import Path


class JSONReader:
    r"""Read fem data from a JSON file.

    The filename is a valid path to a file with extension \*.igo
    """
    def __init__(self, filename=None, accepted=False, file_type='igo'):
        if filename is None or not accepted:
            raise IOError('not a valid input file')
        data = None
        name = filename.split("/")[-1]
        if not os.path.isdir(filename.strip(name)):
            filename = Path(os.getcwd()).child(name)
        if accepted:
            with ZipFile(filename + "." + file_type, 'r') as f:
                json_data_read = f.read('digest.json')
                data = json.loads(json_data_read.decode("utf-8"))
        self._data = data

    @property
    def data(self):
        return self._data


def create(tag):
    r"""

    :param tag:
    :return:
    """
    return Model(tag)


def load(filename):
    r"""

    :param filename:
    :return:
    """
    name = filename.split("/")[-1]
    if not os.path.isdir(filename.strip(name)):
        filename = Path(os.getcwd()).child(name)
    reader = JSONReader(filename=filename, accepted=True)
    data = reader.data
    if data is not None:
        model = create(MODEL)
        model.generate_model(data, model)
        return model
    else:
        return create(MODEL)

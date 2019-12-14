# -*- coding: utf-8 -*-
"""
fem.materials.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from utils import *
from abc import ABC
from utils.node import *


class Materials(Node):
    r"""
    """
    def __init__(self, tag, parent=None):
        super(Materials, self).__init__(tag, parent)
        self._type_info = MATERIALS
        self._valid_children_type = []
        self._dms = {}
        if parent is not None:
            # automatically add class instance to parent if exists
            parent.add_child(self)

    def add(self, tag, selection, prop, expression, **kwargs):
        r"""Add material"""
        if tag not in self._dms.keys():
            self._dms[tag] = {
                'subdomain': dolfin.CompiledSubDomain(selection, tol=1e-14)
            }
        self._dms[tag][prop] = expression

    def component(self):
        r"""Check that the parent is a component."""
        if self._parent is None:
            raise ValueError(error(E_PARENT_NODE_TYPE, None,
                                   self.type_info))
        if not self._parent.type_info == COMPONENT:
            raise ValueError(error(E_PARENT_NODE_TYPE, self._parent.type_info,
                                   self.type_info))
        return self._parent

    def data(self, column):
        pass

    def density(self):
        r""""""
        comp = self.component()
        subdomains = comp.subdomains()
        subdomains.set_all(0)
        ind = 1
        subd = []
        densities = []
        for k, v in self._dms.items():
            self._dms[k]['subdomain'].mark(subdomains, ind)
            subd.append(self._dms[k]['subdomain'])
            if 'density' in self._dms[k].keys():
                densities.append(self._dms[k]['density'])
            else:
                raise ValueError(error(
                    'DENSITY NOT DEFINED FOR MATERIAL {}'.format(k)))
            ind += 1
        return self.Property(subdomains=subd, prop=densities, shape=1)

    def dynamic_viscosity(self):
        r""""""
        comp = self.component()
        subdomains = comp.subdomains()
        subdomains.set_all(0)
        ind = 1
        subd = []
        dynamic_viscosity = []
        for k, v in self._dms.items():
            self._dms[k]['subdomain'].mark(subdomains, ind)
            subd.append(self._dms[k]['subdomain'])
            if 'dynamic_viscosity' in self._dms[k].keys():
                dynamic_viscosity.append(self._dms[k]['dynamic_viscosity'])
            else:
                raise ValueError(error(
                    'DYNAMIC VISCOSITY NOT DEFINED FOR MATERIAL {}'.format(k)))
            ind += 1
        return self.Property(subdomains=subd, prop=dynamic_viscosity, shape=1)

    def set_data(self, column, value):
        pass

    class Property(dolfin.UserExpression, ABC):
        r"""An Expression is a function (field) that can appear as a
        coefficient in a form.

        This version of the evaluation function has an
        additional cell argument which we can use to check on which cell we are
        currently evaluating the function.
        """
        def __init__(self, **kwargs):
            self.subdomains = kwargs["subdomains"]
            self.prop = kwargs["prop"]
            self.shape = kwargs["shape"]

        def eval_cell(self, values, x, cell):
            for i in range(len(self.prop)):
                if self.subdomains[cell.index] == i:
                    values[0] = self.prop[i]

        def value_shape(self):
            return self.shape,

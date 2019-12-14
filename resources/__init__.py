# -*- coding: utf-8 -*-
"""
resources.__init__.py
November 14, 2019
@author Francois Roy
"""
__application__ = 'cfd'
__author__ = 'Francois Roy'
__authoremail__ = 'frns.roy@gmail.com'
__short_description__ = 'A FEM code used to investigate CDF problems.'
__version__ = '2020.1'


# STRINGS
BUILT_IN = 'built_in'
COMPONENT = 'component'
EXPORT = 'export'
FILLET = 'fillet'
GEOMETRY = 'geometry'
GEOMETRY_FEATURE = 'geometry_feature'
IMPORT = 'import'
IPCS = 'ipcs'
LAMINAR_FLOW = 'laminar_flow'
LINE_PLOT = 'line_plot'
MATERIALS = 'materials'
MESH = 'mesh'
MESH_FEATURE = 'mesh_feature'
MODEL = 'model'
NODE = 'node'
OPEN_CASCADE = 'open_cascade'
PHYSICAL = 'physical'
PHYSICS = 'physics'
PHYSICS_FEATURE = 'physics_feature'
PRIMITIVES = 'primitives'
RECTANGLE = 'rectangle'
RESULTS = 'results'
RESULTS_FEATURE = 'result_feature'
SOLVER_FEATURE = 'solver_feature'
STUDY = 'study'

# EXTENSIONS
BND_XDMF = '_bnd.xdmf'
DOM_XDMF = '_dom.xdmf'
VTK = '.vtk'
XDMF = '.xdmf'

# ERROR STRINGS
E_CHILD_NODE_TYPE = ("The child node type '{}' is not a supported children of "
                     "the parent node type '{}'.")
E_CREATE = ("The feature failed to be created with the following error "
            "message:\n{}")
E_DIM = "The dimension must be an integer between 1 and 3."
E_GEOM = "There is no defined geometry node in the parent's children list."
E_GEOM_TAG = "The mesh node has no assigned geometry."
E_QTY = "The entered dimensionality {} is not compatible with {}."
E_PARENT_NODE_TYPE = ("The parent node type '{}' is not valid for child "
                      "type '{}'.")
E_MESH = "There is no defined mesh node in the parent's children list."
E_MESH_TAG = "The physics node has no assigned mesh."
E_NA = "This feature has not been implemented yet."
E_PATH = "The path to {} does not exist."
E_TAG = ("The node with tag '{}' is not in the children list of the "
         "parent '{}'.")
E_VALID = "The value '{}' is not valid for the property '{}'."


def error(error_code, *args):
    r"""Returns the string attached to the error code.

    :param error_code: The error code.
    :param args: optional arguments
    :return: The error message
    """
    return error_code.format(*args)

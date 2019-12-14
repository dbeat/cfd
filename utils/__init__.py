# -*- coding: utf-8 -*-
"""
utils.__init__.py
November 14, 2019
@author Francois Roy
"""
import inspect
from pint import UnitRegistry
from pint.errors import DimensionalityError
import logging
import sympy as sym
import numpy as np
import cppimport
from resources import *
from .util import *

# COMPILED CODE
"""
cppimport looks for a C or C++ source file that matches the requested module. 
If such a file exists, the file is first run through the Mako templating 
system. The compilation options produced by the Mako pass are then use to 
compile the file as a Python extension. The extension (shared library) that 
is produced is placed in the same folder as the C++ source file. Then, 
the extension is loaded. 

A python extension module --> a library of compiled code
pybind11 for C++ to Python bindings. pybind11 is a lightweight header-only 
library that exposes C++ types in Python and vice versa, mainly to create 
Python bindings of existing C++ code.

cppimport combines the process of compiling and importing an extension in 
Python so that you can type module_name = cppimport.imp("module_name") and not 
have to worry about multiple steps.
"""
# cppimport.force_rebuild()  # force rebuild
# cppimport.set_quiet(False)
some_code = cppimport.imp('src.somecode')  # compile and import cpp code

# LOGGING
LOGGING_FORMAT = '%(asctime)-15s %(threadName)s %(levelname)-8s %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)


# UNITS
ureg = UnitRegistry()
Q_ = ureg.Quantity


# PATHS
ROOT_DIR = Path(os.path.abspath(__file__)).ancestor(2)
APP_DIR = ROOT_DIR.child(".cfd")
OUT_DIR = ROOT_DIR.child('outputs')

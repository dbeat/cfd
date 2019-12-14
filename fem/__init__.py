# -*- coding: utf-8 -*-
"""
fem.__init__.py
November 14, 2019
@author Francois Roy
"""
from .component import *
from .geometry import *
from .materials import *
from .mesh import *
from .physics import *
from .study import *
from .results import *
from .geometry_feature import *
from .mesh_feature import *
from .physics_feature import *
from .results_feature import *
from .solver_feature import *
from fem.geom_feats.rectangle import *
from fem.physics_feats.laminar_flow import *
from fem.solver_feats.ipcs import *
from fem.results_feats.line_plot import *
from .model import *

/*
<%
from dolfin.jit.jit import dolfin_pc
setup_pybind11(cfg)
cfg['include_dirs'] = dolfin_pc['include_dirs']
cfg['library_dirs'] = dolfin_pc['library_dirs']
%>
*/
#include "dolfin.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

int square(int x) {
    return x * x;
}


PYBIND11_MODULE(somecode, m) {
    m.doc() = "example plugin";  // optional module docstring
    m.def("square", &square, "A function which compute the square of a number.", py::arg("x"));
}
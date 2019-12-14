# -*- coding: utf-8 -*-
"""
models_2d.axi_symmetric.poiseuille_axi.py
November 14, 2019
@author Francois Roy
"""
import dolfin
from scipy.constants import g

from utils import *
from fem.geom_feats.utils import check_dimension
import fem
from fem.solver_feats.ipcs import Ipcs


class PoiseuilleAxi(fem.Model):
    r"""The unsteady laminar flow of a newtonian, incompressible fluid in
    a circular pipe, termed Poiseuille flow, has an analytical solution.

    we consider here a fluid of constant density :math:`\rho` and viscosity
    :math:`\mu`, flowing in a vertical tube of length :math:`L` and radius
    :math:`R`. The liquid flows downward under the influence of a pressure
    difference and gravity. The tube length is specified to be large  with
    respect to the tube radius, so that end effects will be unimportant
    throughout most of the tube (flow parallel to the tube wall at the inlet
    and outlet).

    We assume a negligible radial component of the velocity, a no-slip
    condition at the wall, i.e. :math:`u_z=0` at
    :math:`r=R`, and axial symmetry, i.e.
    :math:`\frac{\partial u_z}{\partial r}=0`, at :math:`r=0`.

    The equations representing the fluid dynamics are obtained from the
    conservation of mass (continuity) and momentum (Navier-Stokes).

    For incompressible flow, the continuity equation is:

    .. math::  \nabla\cdot \mathbf{u} = 0

    and the Navier-Stokes equation becomes:

    .. math:: \rho\left(\frac{\partial\mathbf{u}}{\partial t} +
        \mathbf{u}\cdot\nabla \mathbf{u}\right) = -\nabla p +
        \nabla\cdot\bar{\tau} + \mathbf{F}

    where :math:`\mathbf{u}` is the fluid velocity,  :math:`p` is the pressure
    and where :math:`\mathbf{F}=\rho\mathbf{g}` is the volume force due to
    gravity. The stress tensor :math:`\bar{\tau}` is denoted by

    .. math:: \bar{\tau} = 2\mu\bar{\epsilon}

    where

    .. math:: \bar{\epsilon} = \frac{1}{2}\left(\nabla \mathbf{u} +
        (\nabla\mathbf{u})^T \right)

    is the strain-rate tensor.

    Note that the Navier-Stokes equations are considered time-dependent.

    **Cylindrical Coordinates**

    The Navier-Stokes equation is written by
    components in cylindrical coordinates (:math:`r,~\theta,~z`):

    :math:`r`-component:

    .. math::  \rho\left(\frac{\partial}{\partial t}u_r+
        u_r\frac{\partial}{\partial r}u_r+\frac{u_\theta}{r}\frac{\partial}
        {\partial \theta}u_r+u_z\frac{\partial}{\partial z}u_r
        -\frac{u_\theta^2}{r}\right) = -\frac{\partial}{\partial r}p +
        \mu\left(\frac{\partial}{\partial r}\left(\frac{1}{r}
        \frac{\partial}{\partial r}(ru_r)\right) +
        \frac{1}{r^2}\frac{\partial^2}{\partial \theta^2}u_r+
        \frac{\partial^2}{\partial z^2}u_r-
        \frac{2}{r^2}\frac{\partial}{\partial \theta}u_\theta\right) +\rho g_r

    :math:`\theta`-component:

    .. math::  \rho\left(\frac{\partial}{\partial t}u_\theta+
        u_r\frac{\partial}{\partial r}u_\theta+\frac{u_\theta}{r}\frac{\partial}
        {\partial \theta}u_\theta+u_z\frac{\partial}{\partial z}u_\theta
        +\frac{u_ru_\theta}{r}\right) = -\frac{1}{r}\frac{\partial}
        {\partial \theta}p +
        \mu\left(\frac{\partial}{\partial r}\left(\frac{1}{r}
        \frac{\partial}{\partial r}(ru_\theta)\right) +
        \frac{1}{r^2}\frac{\partial^2}{\partial \theta^2}u_\theta+
        \frac{\partial^2}{\partial z^2}u_\theta+
        \frac{2}{r^2}\frac{\partial}{\partial \theta}u_r\right) +\rho g_\theta

    :math:`z`-component:

    .. math::  \rho\left(\frac{\partial}{\partial t}u_z+
        u_r\frac{\partial}{\partial r}u_z+\frac{u_\theta}{r}\frac{\partial}
        {\partial \theta}u_z+u_z\frac{\partial}{\partial z}u_z\right)
         = -\frac{\partial}
        {\partial z}p +
        \mu\left(\frac{1}{r}\frac{\partial}{\partial r}\left(r
        \frac{\partial}{\partial r}u_z\right) +
        \frac{1}{r^2}\frac{\partial^2}{\partial \theta^2}u_z+
        \frac{\partial^2}{\partial z^2}u_z\right) +\rho g_z


    The continuity equation in cylindrical component is:

    .. math:: \frac{1}{r}\left(\frac{\partial}{\partial r}(ru_r)
        +\frac{\partial}{\partial \theta}(u_\theta)\right) +
        \frac{\partial}{\partial z} u_z = 0

    **Axisymmetric Formulation**

    In an axisymmetric model there is no gradient in the azimuthal
    direction :math:`\theta`. If we also assume that the
    :math:`\theta`-component of the velocity field is zero, the
    :math:`\theta`-component of the Navier-Stokes equation is removed and
    the continuity/momentum equations become:

    Continuity:

    .. math:: \frac{u_r}{r}+\frac{\partial}{\partial r}u_r
        + \frac{\partial}{\partial z} u_z = 0

    Navier-Stokes, :math:`r`-component:

    .. math::  \rho\left(\frac{\partial}{\partial t}u_r+
        u_r\frac{\partial}{\partial r}u_r
        +u_z\frac{\partial}{\partial z}u_r\right)
         = -\frac{\partial}{\partial r}p +
        \mu\left(\frac{\partial}{\partial r}\left(\frac{u_r}{r}+
        \frac{\partial}{\partial r}u_r\right) +
        \frac{\partial^2}{\partial z^2}u_r\right)

    Navier-Stokes, :math:`z`-component:

    .. math::  \rho\left(\frac{\partial}{\partial t}u_z+
        u_r\frac{\partial}{\partial r}u_z
        +u_z\frac{\partial}{\partial z}u_z\right)
         = -\frac{\partial}
        {\partial z}p +
        \mu\left(\frac{1}{r}\frac{\partial}{\partial r}\left(r
        \frac{\partial}{\partial r}u_z\right) +
        \frac{\partial^2}{\partial z^2}u_z\right) +\rho g_z

    Note that the gravity term only have a :math:`z`-component.

    :param tag: The model name -- default pa
    :param size: The radius and length of the pipe [radius, height],
      --default 20 mm and 100 mm.
    :param mu: Dynamic viscosity -- default 8.548e-4 Pa.s (water 300 K).
    :param rho: Density -- default 996.534 kg/m3 (water 300 K).
    :param pin: Inlet pressure -- default 8 Pa.
    :param pout: Outlet pressure -- default 0 Pa.
    :param ne_r: Number of element along the radius of the pipe -- default 10.
    :param ne_z: Number of element along the height of the pipe -- default 100.
    """
    def __init__(self, tag='pa', size=Q_(np.asarray([20.0, 100.0]), "mm"),
                 mu=Q_(8.548e-4, 'Pa*s'), rho=Q_(996.534, 'kg/m**3'),
                 pin=Q_(8.0, 'Pa'), pout=Q_(0.0, 'Pa'), ne_r=10, ne_z=100):
        super(PoiseuilleAxi, self).__init__(tag)
        self._size = size.to("m")
        self._mu = mu.to("Pa*s")
        self._rho = rho.to("kg/m**3")
        self._pin = pin.to('Pa')
        self._pout = pout.to('Pa')
        self._ne_r = int(ne_r)
        self._ne_z = int(ne_z)
        self.add_child(fem.Component('comp', 2, is_axi=True))
        self._geom = self.geom()
        self._mesh = self.mesh()

    @property
    def size(self):
        r"""The dimensions of the pipe [radius, height]"""
        return self._size

    @size.setter
    def size(self, value):
        # raise invalid syntax if can't convert to string
        name = inspect.stack()[0][3]
        if len(value) != 2:
            raise ValueError("not a valid number of arguments")
        for i in range(2):
            check_dimension(value, name)
        self._size = value.to('m')

    def axial_line(self):
        r"""Define an axial line on which the solution :math:`p` can be
        mapped (interpolated)."""
        z = self._size[1].magnitude
        return Q_(np.linspace(0, z, self._ne_z + 1), 'm')

    def compute(self, t_end=Q_(10.0, 's'), num_steps=500):
        r"""For incompressible flow, the continuity equation is:

        .. math::  \nabla\cdot \mathbf{u} = 0

        and the Navier-Stokes equation becomes:

        .. math:: \rho\left(\frac{\partial\mathbf{u}}{\partial t} +
            \mathbf{u}\cdot\nabla \mathbf{u}\right) =
            \nabla\cdot\bar{\pi} + \mathbf{F}

        where :math:`\mathbf{u}` is the fluid velocity,  :math:`p` is the
        pressure and where :math:`\mathbf{F}=\rho\mathbf{g}` is the volume
        force due to gravity. The molecular stress tensor :math:`\bar{\pi}` is
        denoted by:

        .. math:: \bar{\pi} = \bar{\tau} - p\bar{I}, \quad \bar{I}\textrm{ is
            the unit tensor}

        where :math:`\bar{\tau}` is the viscous stress tensor defined by:

        .. math:: \bar{\tau} = 2\mu\bar{\epsilon}

        and where

        .. math:: \bar{\epsilon} = \frac{1}{2}\left(\nabla \mathbf{u} +
            (\nabla\mathbf{u})^T \right)

        is the strain-rate tensor.

        The variational formulation of the viscous term is:

        .. math:: \int_\Omega \left(\nabla\cdot\bar{\pi}\right)\cdot
            \mathbf{v}d\mathbf{x}

        Since the term :math:`\nabla\cdot\bar{\pi}` contains second-order
        derivatives of the velocity field :math:`\mathbf{u}`, we integrate this
        term by parts:

        .. math:: -\int_\Omega\left(\nabla\cdot\bar{\pi}\right)\cdot
            \mathbf{v}d\mathbf{x} = \int_\Omega \bar{\pi}:\nabla
            \mathbf{v}d\mathbf{x}-\int_{\delta\Omega}\left(\bar{\pi}
            \cdot\hat{\mathbf{n}}\right)\cdot\mathbf{v}ds

        where the colon operator is the inner product (Frobenius inner-product)
        between tensors, and :math:`\hat{\mathbf{n}}` is the outward unit
        normal at the boundary (traction, or stress vector).

        In cylindrical coordinates (:math:`r,~ \theta,~ z`), the gradient of
        the velocity field :math:`\mathbf{u}` writes

        .. math:: \nabla\cdot{\mathbf{u}} = \left(
            \begin{array}{ccc}
              \frac{\partial u_r}{\partial r} &
              \frac{\partial u_\theta}{\partial r} &
              \frac{\partial u_z}{\partial r}\\
              \frac{1}{r}\frac{\partial u_r}{\partial \theta}-
              \frac{u_\theta}{r}&
              \frac{1}{r}\frac{\partial u_\theta}{\partial \theta}+
               \frac{u_r}{r}&
              \frac{1}{r}\frac{\partial u_z}{\partial \theta}\\
              \frac{\partial u_r}{\partial z} &
              \frac{\partial u_\theta}{\partial z} &
              \frac{\partial u_z}{\partial z}
            \end{array}
            \right)

        The strain-rate tensor :math:`\bar{\epsilon}` is then:

        .. math:: \bar{\epsilon} = \left(
            \begin{array}{ccc}
              \frac{\partial u_r}{\partial r} &
              \frac{1}{2}\left(\frac{\partial u_\theta}{\partial r} +
              \frac{1}{r}\frac{\partial u_\theta}{\partial \theta}-
               \frac{u_\theta}{r}\right)&
              \frac{1}{2}\left(\frac{\partial u_z}{\partial r}+
              \frac{\partial u_r}{\partial z}\right)\\
              \frac{1}{2}\left(\frac{1}{r}\frac{\partial u_r}{\partial \theta}-
              \frac{u_\theta}{r}+\frac{\partial u_\theta}{\partial r}\right)&
              \frac{1}{r}\frac{\partial u_\theta}{\partial \theta}+
               \frac{u_r}{r}&
              \frac{1}{2}\left(\frac{1}{r}\frac{\partial u_z}{\partial
              \theta}+\frac{\partial u_\theta}{\partial z}\right)\\
              \frac{1}{2}\left(\frac{\partial u_r}{\partial z}
              +\frac{\partial u_z}{\partial r}\right)&
              \frac{1}{2}\left(\frac{\partial u_\theta}{\partial z}
              +\frac{1}{r}\frac{\partial u_z}{\partial \theta}\right)&
              \frac{\partial u_z}{\partial z}
            \end{array}
            \right)

        From the definition above, the viscous stress tensor :math:`\bar{\tau}`
        is:

        .. math:: \bar{\tau} = \mu\left(
            \begin{array}{ccc}
              2\frac{\partial u_r}{\partial r} &
              \frac{\partial u_\theta}{\partial r} +
              \frac{1}{r}\frac{\partial u_\theta}{\partial \theta}-
               \frac{u_\theta}{r}&
              \frac{\partial u_z}{\partial r}+
              \frac{\partial u_r}{\partial z}\\
              \frac{1}{r}\frac{\partial u_r}{\partial \theta}-
              \frac{u_\theta}{r}+\frac{\partial u_\theta}{\partial r}&
              2\left(\frac{1}{r}\frac{\partial u_\theta}{\partial \theta}+
               \frac{u_r}{r}\right)&
              \frac{1}{r}\frac{\partial u_z}{\partial
              \theta}+\frac{\partial u_\theta}{\partial z}\\
              \frac{\partial u_r}{\partial z}
              +\frac{\partial u_z}{\partial r}&
              \frac{\partial u_\theta}{\partial z}
              +\frac{1}{r}\frac{\partial u_z}{\partial \theta}&
              2\frac{\partial u_z}{\partial z}
            \end{array}
            \right)

        and the molecular stress tensor :math:`\bar{\pi}` is:

        .. math:: \bar{\pi} = \mu\left(
            \begin{array}{ccc}
              2\frac{\partial u_r}{\partial r} -\frac{p}{\mu}&
              \frac{\partial u_\theta}{\partial r} +
              \frac{1}{r}\frac{\partial u_\theta}{\partial \theta}-
               \frac{u_\theta}{r}&
              \frac{\partial u_z}{\partial r}+
              \frac{\partial u_r}{\partial z}\\
              \frac{1}{r}\frac{\partial u_r}{\partial \theta}-
              \frac{u_\theta}{r}+\frac{\partial u_\theta}{\partial r}&
              2\left(\frac{1}{r}\frac{\partial u_\theta}{\partial \theta}+
               \frac{u_r}{r}\right) -\frac{p}{\mu} &
              \frac{1}{r}\frac{\partial u_z}{\partial
              \theta}+\frac{\partial u_\theta}{\partial z}\\
              \frac{\partial u_r}{\partial z}
              +\frac{\partial u_z}{\partial r}&
              \frac{\partial u_\theta}{\partial z}
              +\frac{1}{r}\frac{\partial u_z}{\partial \theta}&
              2\frac{\partial u_z}{\partial z} -\frac{p}{\mu}
            \end{array}
            \right)

        The scalar product (or double dot product) of two tensors is the
        summed pairwise product of all element of the tensors, i.e.

        .. math:: \bar{\pi}:\nabla\mathbf{v} =
            \pi_{rr}\frac{\partial v_r}{\partial r}+
            \pi_{r\theta}\frac{\partial v_\theta}{\partial r}+\ldots +
            \pi_{zz}\frac{\partial v_z}{\partial z}

        and the vector product (or dot product) of a tensor with a vector is
        just the regular product between a matrix and a vector.

        .. math:: \bar{\pi}\cdot \hat{\mathbf{n}} = \left(\pi_{rr}n_r+
            \pi_{r\theta}n_\theta + \pi_{rz}nz\right) \hat{\mathbf{e}}_r +
            \left(\pi_{\theta r}n_r + \dots\right)\hat{\mathbf{e}}_\theta +
            \left(\ldots + \pi_{r\theta}n_\theta\right)\hat{\mathbf{e}}_z

        **Axisymmetric Formulation**

        We consider a solid of revolution around a fixed axis (Oz), the
        loading, boundary conditions and material properties are invariant
        with respect to a rotation along the symmetry axis. The solid
        cross-section in a plane :math:`\Theta=` cst is represented by
        a two-dimensional domain :math:`\omega` for which the first spatial
        variable (x[0] in FEniCS) will represent the radial coordinate
        :math:`r` whereas the second spatial variable will denote the axial
        variable :math:`z`.

        In axisymmetric conditions, the full 3D domain :math:`\Omega` can be
        decomposed as :math:`\Omega=\omega\times[0;2\pi]` where the interval
        represents the :math:`\theta` variable. The integration measures
        therefore reduce to :math:`dx=d\omega\cdot(rd\theta)` and
        :math:`dS=ds\cdot(rd\theta)` where :math:`dS` is the surface
        integration measure on the 3D domain :math:`\Omega` and :math:`ds` its
        counterpart on the cross-section boundary :math:`\partial\omega`.

        Exploiting the invariance of all fields with respect to :math:`\theta`,
        we get the variational formulation of the viscous term as:

         .. math:: -\int_\Omega\left(\nabla\cdot\bar{\pi}\right)\cdot
            \mathbf{v}d\mathbf{x} = 2\pi\int_\omega \bar{\pi}:\nabla
            \mathbf{v}rd\omega-2\pi\int_{\delta\omega}\left(\bar{\pi}
            \cdot\hat{\mathbf{n}}\right)\cdot\mathbf{v}r ds

        For an axisymmetric model there is no gradient in the azimuthal
        direction :math:`\theta`. If we also assume that the
        :math:`\theta`-component of the velocity field is zero, we obtain
        the gradient of the velocity field:

        .. math:: \nabla\cdot{\mathbf{u}} = \left(
            \begin{array}{ccc}
              \frac{\partial u_r}{\partial r} &
              0 &
              \frac{\partial u_z}{\partial r}\\
              0&
               \frac{u_r}{r}&
              0\\
              \frac{\partial u_r}{\partial z} &
              0&
              \frac{\partial u_z}{\partial z}
            \end{array}
            \right)

        and the following strain-rate tensor:

        .. math:: \bar{\epsilon} = \left(
            \begin{array}{ccc}
              \frac{\partial u_r}{\partial r} &
              0&
              \frac{1}{2}\left(\frac{\partial u_z}{\partial r}+
              \frac{\partial u_r}{\partial z}\right)\\
              0&
               \frac{u_r}{r}&
              0\\
              \frac{1}{2}\left(\frac{\partial u_r}{\partial z}
              +\frac{\partial u_z}{\partial r}\right)&
              0&
              \frac{\partial u_z}{\partial z}
            \end{array}
            \right)

        *Note*: The vector function space dimension is now two-dimensional.
        We can keep the 3D tensor notation if we perform the integrands
        manually before assembling the bilinear and linear forms.

        *Note*: The factor :math:`u_r/r` is problematic for
        :math:`r\approx 0`. One solution is to ...

        for axisymmetric flow, the velocity field is composed of two
        components, i.e.

        .. math:: \mathbf{u} = u_r\hat{\mathbf{e}}_r+u_z\hat{\mathbf{e}}_z

        **Splitting Method**:

        To overcome the saddle-point problems resulting from a direct
        discretization of the Navier-Stokes equations we use a splitting scheme
        where the velocity and pressure variables are computed in a sequence of
        predictor-corrector type steps.

        Incremental Pressure Correction Scheme (IPCS) -- see :cite:`Logg2012`
        for details of the algorithm.

        In summary, we may thus solve the incompressible Navier-Stokes
        equations efficiently by solving a sequence of three linear
        variational problems in each time step.

        In order to simulate steady-state use t_end = large number

        :param t_end: Final time, default = 10 s.
        :type t_end: ureg.Quantity
        :param num_steps: Number of time steps, default = 500.
        :type num_steps: int
        :return: The solution.
        """
        out = None
        dt = t_end.to('s').magnitude / num_steps
        radius = self._size[0].magnitude
        length = self._size[1].magnitude
        mu = self._mu.magnitude
        rho = self._rho.magnitude
        pin = self._pin.magnitude

        # TODO: something is odd with this mesh, needs investigations
        mesh = self._mesh

        dom = dolfin.cpp.mesh.MeshFunctionSizet(mesh, mesh.mvc_dom())
        bnd = dolfin.cpp.mesh.MeshFunctionSizet(mesh, mesh.mvc_bnd())
        dx = dolfin.Measure("dx", domain=mesh, subdomain_data=dom)
        ds = dolfin.Measure("ds", domain=mesh, subdomain_data=bnd)
        return out

    def exact_solution(self):
        r"""This method is used to validate the finite element model.

        Here we assume that the flow is directed along the
        :math:`z`-direction (parallel to the tube walls), which leads to
        :math:`u_r=0`. The only external force acting on the fluid is gravity
        (:math:`\mathbf{F}\textrm{ext}=-\rho g_z\mathbf{\hat{e}}_z`).

        Using the axisymmetric formulation we have:

        continuity:

        .. math:: \frac{\partial}{\partial z} u_z = 0

        Navier-Stokes, :math:`r`-component:

        .. math::  \frac{\partial}{\partial r}p = 0

        Navier-Stokes, :math:`z`-component:

        .. math::  \rho\frac{\partial}{\partial t}u_z
             = -\frac{\partial}
            {\partial z}p +
            \mu\left(\frac{1}{r}\frac{\partial}{\partial r}\left(r
            \frac{\partial}{\partial r}u_z\right)\right) - \rho g_z

        When steady-state is reached, the term
        :math:`\frac{\partial}{\partial t}u_z=0`. Using the product rule
        we have:

        .. math::  \frac{\partial}{\partial z}p =
            \mu\left(\frac{1}{r}\frac{\partial}{\partial r}u_z +
            \frac{\partial^2}{\partial r^2}u_z
            \right)-\rho g_z

        with the following change of variable:

        .. math:: \phi = r\frac{\partial u_z}{\partial r}

        we have

        .. math:: \frac{\partial \phi}{\partial r} &=
            \frac{\partial u_z}{\partial r} +
            r\frac{\partial^2u_z}{\partial r^2}\\
            &= \frac{\phi}{r} + r\frac{\partial^2u_z}{\partial r^2}

        and

        .. math::  \frac{\partial}{\partial z}p =
            \mu\left(\frac{1}{r}\frac{\partial \phi}{\partial r}\right)-
            \rho g_z

        From :math:`\frac{\partial u_z}{\partial z} = 0`
        (:math:`\frac{\partial \phi}{\partial z} = 0`) and
        :math:`\frac{\partial p}{\partial r} = 0` we can solve the above
        equation by separation of variable, i.e.

        .. math::  \int dp =\int \left(\mu\left(\frac{1}{r}
            \frac{\partial \phi}{\partial r}\right)-\rho g_z\right)dz

        .. math::  \Delta p =
            \left(\mu\left(\frac{1}{r}\frac{\partial \phi}{\partial r}
            \right)-\rho g_z\right)\Delta z

        .. math::  \frac{\Delta p+
            \rho g_z\Delta z}{\mu \Delta z} =
            \frac{1}{r}\frac{\partial \phi}{\partial r}

        Where :math:`\Delta p = p(z=L+z_0) - p(z=z_0)`, and where
        :math:`\Delta z = z_0+L - z_0 = L`.

        By another separation of variable

        .. math::  \int \frac{\Delta p+
            \rho g_z\Delta z}{\mu \Delta z} r dr =
            \int d\phi

        which gives

        .. math::  \phi = \frac{1}{2}\frac{\Delta p+
            \rho g_z\Delta z}{\mu \Delta z}r^2 + C_1

        at :math:`r=0` we have :math:`\phi(0)=0` and :math:`C_1=0`.
        Substituting the value of :math:`\phi` in the above equation yields to:

        .. math::  r\frac{\partial u_z}{\partial r} = \frac{1}{2}
            \frac{\Delta p+\rho g_z\Delta z}{\mu \Delta z}r^2

        Integrating again on both sides gives:

        .. math::  u_z = \frac{1}{4}
            \frac{\Delta p+\rho g_z\Delta z}{\mu \Delta z}r^2 + C_2

        with :math:`u_z=0` at :math:`r=R`, we get

        .. math:: C_2 = -\frac{1}{4}
            \frac{\Delta p+\rho g_z\Delta z}{\mu \Delta z}r^2

        and

        .. math:: u_z = \frac{1}{4}
            \frac{\Delta p+\rho g_z\Delta z}{\mu \Delta z}\left(r^2-R^2\right)

        Rearranging the terms we get

        .. math:: u_z &= \frac{1}{4}
            \frac{p(z=L)-p(z=z_0)+(\rho g_z(L-z_0)-\rho g_zz_0)}{\mu L}
            \left(r^2-R^2\right)\\
            &= \frac{1}{4}
            \frac{(p(z=L)+\rho g_z(L-z_0))-(p(z=z_0)+\rho g_z z_0)}
            {\mu L}R^2\left(\left(\frac{r}{R}\right)^2-1\right)\\
            &=\frac{1}{4}
            \frac{\mathcal{P}_L-\mathcal{P}_0}
            {\mu L}R^2\left(\left(\frac{r}{R}\right)^2-1\right)\\
            &=\frac{1}{4}
            \frac{\mathcal{P}_0-\mathcal{P}_L}
            {\mu L}R^2\left(1-\left(\frac{r}{R}\right)^2\right)

        where :math:`\mathcal{P}_L=p(z=L)+\rho g_z(L-z_0)` and
        :math:`\mathcal{P}_0=p(z=z_0)+\rho g_zz_0`

        The pressure can be obtained using the Navier-Stokes,
        :math:`z`-component equation and the axial velocity :math:`u_z`,
        giving:

        .. math:: p = p(z=z_0) - \left(p(z=z_0)-p(z=L)\right)\frac{z}{L}

        For more info see :cite:`BSL2007` p. 88.

        :return: The solution, i.e. :math:`(p, u_z)` respectively along the
          center of the pipe line (symmetry axis), and along the radial
          distance.
        """
        radius = self._size[0]
        height = self._size[1]
        mu = self._mu
        rho = self._rho
        pin = self._pin
        pout = self._pout
        z = self.axial_line()
        r = self.radial_line()
        pl = pin + rho * Q_(g, 'm/s**2') * height
        p0 = pout + rho * Q_(g, 'm/s**2') * height
        uz = 0.25 * (p0 - pl) / mu / height * radius**2 * (1 - (r / radius)**2)
        p = pout - (pout - pin) * z / height
        uz = uz.to('m/s')
        p = p.to('Pa')
        return p, uz

    def geom(self):
        r""""""
        geom = self.component('comp').create(GEOMETRY, 'geom')
        geom.create(RECTANGLE, tag='r1', a=self._size[0], b=self._size[1])
        geom.run()
        return geom

    def mesh(self):
        r""""""
        if self._geom is not None:
            geom = self._geom
        else:
            geom = self.geom()
            self._geom = geom
        mesh = self.component('comp').create(MESH, 'mesh', geom_tag=geom.tag)
        mesh.run()
        return mesh

    def molecular_stress_tensor(self, u, p):
        r"""Define the molecular stress tensor:

        .. math:: \bar{\pi} = 2\mu\bar{\epsilon}-p\bar{I}

        :param u: The velocity field.
        :param p: The pressure field.
        :return: The molecular stress tensor.
        """
        mu = self._mu.magnitude
        return 2 * mu * self.strain_rate_tensor(u) - p * dolfin.Identity(3)

    def radial_line(self):
        r"""Define a radial line on which the solution :math:`u_z` can be
        mapped (interpolated)."""
        r = self._size[0].magnitude
        return Q_(np.linspace(0, r, self._ne_r + 1), 'm')

    def strain_rate_tensor(self, u):
        r"""Define the symmetric strain-rate tensor

        :param u: The velocity field (2D).
        :return: The strain rate tensor.
        """
        r = dolfin.SpatialCoordinate(self._mesh)[0]
        ur = u[0]
        uz = u[1]
        ur_r = ur.dx(0)
        ur_z = ur.dx(1)
        uz_r = uz.dx(0)
        uz_z = uz.dx(1)
        return dolfin.sym(
            dolfin.as_tensor(
                [
                    [ur_r, 0, 0.5 * (uz_r + ur_z)],
                    [0, ur / r, 0],
                    [0.5 * (uz_r + ur_z), 0, uz_z]
                ]))

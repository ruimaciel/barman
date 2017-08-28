"""
    This file is part of Barman.

    Copyright 2017 by Rui Maciel <rui.maciel@gmail.com>

    Barman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Barman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Barman.  If not, see <http://www.gnu.org/licenses/>.
"""

from abc import ABCMeta, abstractmethod

import numpy
from math import sin, cos
from numpy.linalg import norm
from barman.dofs import Parameter, GlobalDoF
from barman.sections import Section


class BarElement(metaclass=ABCMeta):
    """Defines the abstract base class used by all elements"""

    def __init__(self, nodes, section, material):
        self._nodes = nodes # two nodes: start node, and end node
        self._section = section
        self._material = material
        

    @property
    def nodes(self):
        return self._nodes

    @property
    def section(self):
        return self._section

    @property
    def material(self):
        return self._material

    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    def get_global_dofs(self):
        """Returns a list with the element's global degrees of freedom (DoF)"""
        pass

    @abstractmethod
    def get_transformation_matrix(self):
        """Returns the transformation matrix that transforms local coordinates into global coordinates"""
        pass

    @abstractmethod
    def get_local_stiffness_matrix(self):
        """Returns the element's stiffness matrix represented in the local coordinate system"""
        pass


    def get_global_stiffness_matrix(self):
        """Returns the element's stiffness matrix represented in the global coordinate system"""

        T = self.get_transformation_matrix();
        k_local = self.get_local_stiffness_matrix();
        k_global = numpy.dot( numpy.transpose(T), k_local).dot(T)

        return k_global



class Bar2(BarElement):
    """Bar2 beam element"""

    def get_global_dofs(self):
        """Returns a list with the element's global degrees of freedom (DoF)"""

        parameters = [ Parameter.dx, Parameter.dy]
        global_dofs = [ GlobalDoF(node, parameter) for node in self.nodes for parameter in parameters]
        return global_dofs


    def get_length(self):
        """Returns the length between end nodes"""

        xi = numpy.array(self.nodes[0].position)
        xf = numpy.array(self.nodes[-1].position)
        return norm(xf-xi)


    def get_shape_functions(self, x):
        """Returns the shape function's values evaluated at x"""

        L = self.get_length()

        N = numpy.array([1-x/L, x/L]);

        return N
        

    def get_local_stiffness_matrix(self):
        """Returns the element's stiffness matrix represented in the local coordinate system"""

        E = self.material.young_modulus
        EA = E*self.section.area
        L = self.get_length()

        k = numpy.array(
            [[  EA/L, -EA/L],
             [ -EA/L,  EA/L]]
        )

        return k


    def get_local_mass_matrix(self):
        """Returns the element's mass matrix represented in the local coordinate system"""
        
        A = self.section.area
        rho = self.material.density
        L = self.get_length()
        
        rAL6 = rho*A*L/6.0
        
        m = rAL6*numpy.array(
            [[  2.0,  1.0],
             [  1.0,  2.0]]
        )

        return m


    def get_transformation_matrix(self):
        """Returns the transformation matrix that transforms local coordinates into global coordinates"""

        nodes = self.nodes
        nf = numpy.array(nodes[-1].position)
        ni = numpy.array(nodes[0].position)
        r = nf-ni
        L = self.get_length()
        director_cosines = r/L
        c = director_cosines[0]
        s = director_cosines[1]

        T = numpy.array(
            [[c, s, 0, 0],
             [0, 0, c, s]] )

        return T



class EulerBernoulli(BarElement):
    """Euler-Bernoulli (engineering) beam element"""

    def get_global_dofs(self):
        """Returns a list with the element's global degrees of freedom (DoF)"""

        parameters = [ Parameter.dx, Parameter.dy, Parameter.rz ]
        global_dofs = [ GlobalDoF(node, parameter) for parameter in parameters for node in self.nodes]
        return global_dofs


    def get_length(self):
        """Returns the length between end nodes"""

        xi = numpy.array(self.nodes[0].position)
        xf = numpy.array(self.nodes[-1].position)
        return norm(xf-xi)


    def get_shape_functions(self, x):
        """Returns the shape function's values evaluated at x"""

        L = self.get_length()

        xi = x/L

        N = numpy.array([1-xi,
        1-3*xi**2 + 2*xi**3,
        L*(xi - 2*xi**2 + xi**3),
        xi,
        3*xi**2 - 2*xi**3,
        L*(3*xi**3-x**2) ])

        return N
        

    def get_local_stiffness_matrix(self):
        """Returns the element's stiffness matrix represented in the local coordinate system"""

        E = self.material.young_modulus
        EI = E*self.section.I_zz
        EA = E*self.section.area
        L = self.get_length()

        k = numpy.array(
           [ 
            [   EA/L,        0,           0,      -EA/L,      0,           0       ],
            [    0,      12*EI/L**3,   6*EI/L**2,   0,   -12*EI/L**3,   6*EI/L**2  ],
            [    0,       6*EI/L**2,   4*EI/L,      0,    -6*EI/L**2,   2*EI/L     ],
            [  -EA/L,        0,           0,       EA/L,      0,           0       ],
            [    0,     -12*EI/L**3,  -6*EI/L**2,   0,    12*EI/L**3,  -6*EI/L**2  ],
            [    0,       6*EI/L**2,   2*EI/L,      0,    -6*EI/L**2,   4*EI/L     ]]
        )

        return k


    def get_local_mass_matrix(self):
        """Returns the element's mass matrix represented in the local coordinate system"""
        
        A = self.section.area
        rho = self.material.density
        L = self.get_length()
        
        rAL420 = rho*A*L/420.0
        
        m = rAL420*numpy.array(
            [
             [140.0,    0.0,     0.0,       70.0,     0.0,       0.0     ],
             [  0.0,  156.0,    22.0*L,      0.0,    54.0,     -13.0*L   ],
             [  0.0,   22.0*L,   4.0*L*L,    0.0,    13.0*L,    -3.0*L*L ],
             [ 70.0,    0.0,     0.0,      140.0,     0.0,       0.0     ],
             [  0.0,   54.0,    13.0*L,      0.0,   156.0,     -22.0*L   ],
             [  0.0,  -13.0*L,  -3.0*L*L,    0.0,   -22.0*L,     4.0*L*L ]]
        )

        return m



    def get_transformation_matrix(self):
        """Returns the transformation matrix that transforms local coordinates into global coordinates"""

        nodes = self.nodes
        nf = numpy.array(nodes[-1].position)
        ni = numpy.array(nodes[0].position)
        r = nf-ni
        L = self.get_length()
        director_cosines = r/L
        c = director_cosines[0]
        s = director_cosines[1]

        T = numpy.array(
            [[ c, s, 0,  0, 0, 0],
             [-s, c, 0,  0, 0, 0],
             [ 0, 0, 1,  0, 0, 0],
             [ 0, 0, 0,  c, s, 0],
             [ 0, 0, 0, -s, c, 0],
             [ 0, 0, 0,  0, 0, 1]]
             )

        return T


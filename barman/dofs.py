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

from enum import Enum
from math import sin, cos
import numpy


class Parameter(Enum):
    """Determines the types of parameters (input and output) supported by barman.
    
    Attributes:
        dx: displacement along the XX axis
        dy: displacement along the YY axis
        rz: rotation along the ZZ axis
        fx: force along the XX axis
        fy: force along the YY axis
        mz: moment along the ZZ axis
    """

    dx = 0
    dy = 1
    rz = 2
    fx = 3
    fy = 4
    mz = 5


class CoordinateSystem:
    """A coordinate system"""

    def __init__(self, angle = 0):
        self.set_angle(angle)


    def set_angle(self, angle):
        """Sets the rotation angle (in radians)""" 

        self._angle = angle


    def get_transformation(self):
        
        c = cos(self._angle)
        s = sin(self._angle)

        T = numpy.array(
           [[  c, s, 0],
            [ -s, c, 0],
            [  0, 0, 1.0]]
        )

        return T

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._angle == other._angle
        return false

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._angle)


class Node:
    """A point in a 2D space used to defined degrees of freedom (DoF)"""

    def __init__(self, position):
        self._position = position
        self._coordinate_system = CoordinateSystem()
        

    @property
    def position(self):
        return self._position


    @property
    def coordinate_system(self):
        return self._coordinate_system

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.position == other.position and self.coordinate_system == other.coordinate_system
        return false

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Node({},{})".format(self.position[0], self.position[1])

    def __hash__(self):
        return hash( tuple(self._position) + (hash(self._coordinate_system), ) )


class GlobalDoF:
    """Represents a degree of freedom (DoF) of a global model"""

    def __init__(self, node, parameter):
        self._node = node
        self._parameter = parameter

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._node == other._node and self._parameter == other._parameter
        return false

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "GlobalDof( ({},{}), {})".format(self._node.position[0], self._node.position[1], self._parameter)

    def __hash__(self):
        return hash( ( hash(self._node), self._parameter) )


class GlobalDoFLink:
    """Links two GlobalDoF objects so that they are handled as the same GlobalDoF"""

    def __init__(self, global_dof):
        self._global_dofs = global_dof



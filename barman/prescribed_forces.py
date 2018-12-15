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


class PrescribedForce:
    """Prescribes the force associated with a global degree of freedom (DoF)"""

    def __init__(self, global_dof, value):
        self._global_dof = global_dof
        self._value = value

    @property
    def global_dof(self):
        return self._global_dof

    @property
    def value(self):
        return self._value

    def get_values(self):
        return [(self._global_dof, self._value)]

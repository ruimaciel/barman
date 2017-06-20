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

from barman import prescribed_displacements
from barman import prescribed_forces


class LinearStatic:
    """A linear static analysis model"""

    def __init__(self):
        self.clear()


    def clear(self):
        """Clears all attributes."""

        self._elements = []
        self._prescribed_displacements = []
        self._prescribed_forces = []
        self._global_dof_links = [] # links between GlobalDoFs
        

    def append_element(self, element):
        """Appends an element to the element list"""

        self._elements.append(element)


    @property
    def elements(self):
        """Get the element list."""

        return self._elements


    def append_prescribed_displacement(self, prescribed_displacement):
        """Appends a prescribed displacement to the element list"""

        if not isinstance(prescribed_displacement, prescribed_displacements.PrescribedDisplacement):
            raise TypeError('prescribed displacement must be a PrescribedDisplacement')

        self._prescribed_displacements.append(prescribed_displacement)


    def append_prescribed_force(self, prescribed_force):
        """Appends an element to the element list"""

        if not isinstance(prescribed_force, prescribed_forces.PrescribedForce):
            raise TypeError('prescribed force must be a PrescribedForce')

        self._prescribed_forces.append(prescribed_force)


    @property
    def prescribed_displacements(self):
        """Get the prescribed displacements list."""

        return self._prescribed_displacements


    @property
    def prescribed_forces(self):
        """Get the prescribed forces list."""

        return self._prescribed_forces


    def append_global_dof_link(self, global_dof_link):
        """Appends a link between global degrees of freedom (DoF)"""

        self._global_dof_links.append(global_dof_link)


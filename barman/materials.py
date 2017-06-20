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


class LinearElastic:
    """Represents a linear elastic material"""


    def __init__(self, name, young_modulus, poisson_ratio):
        self._name = name
        self._young_modulus = young_modulus
        self._poisson_ratio = poisson_ratio
        self._density = 0.0

    @property
    def young_modulus(self):
        return self._young_modulus

    @property
    def poisson_ratio(self):
        return self._poisson_ratio

    @property
    def density(self):
        return self._density


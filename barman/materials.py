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


    def __init__(self, name: str, young_modulus: float, poisson_ratio: float):
        self._name: str = name
        self._young_modulus: float = young_modulus
        self._poisson_ratio: float = poisson_ratio
        self._density: float = 0.0

    @property
    def young_modulus(self) -> float:
        return self._young_modulus

    @property
    def poisson_ratio(self) -> float:
        return self._poisson_ratio

    @property
    def density(self) -> float:
        return self._density


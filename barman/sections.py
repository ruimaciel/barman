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


class Section:
    """The cross-section of a bar element"""


    def __init__(self, area, I_zz):
        self._area = area
        self._I_zz = I_zz

    @property
    def area(self):
        return self._area

    @property
    def I_zz(self):
        return self._I_zz


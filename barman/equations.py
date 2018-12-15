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

import numpy
import scipy.sparse
from scipy.sparse import dok_matrix, coo_matrix

class LinearStatic:
    """The equation of a linear static analysis problem"""

    def __init__(self, dof_map, k_global, d_global, f_global, essential_global_dofs):
        self.clear()
        self._dof_map = dof_map
        self.set_equation(dof_map, k_global, d_global, f_global, essential_global_dofs);

    def clear(self):
        self._dof_map = []
        self._k_ff = []
        self._k_fe = []
        self._k_ef = []
        self._k_ee = []
        self._d_e = []
        self._d_f = []
        self._f_e = []
        self._f_f = []


    @property
    def k_ff(self):
        return self._k_ff

    @property
    def k_fe(self):
        return self._k_fe

    @property
    def k_ef(self):
        return self._k_ef

    @property
    def k_ee(self):
        return self._k_ee

    @property
    def f_f(self):
        return self._f_f

    @property
    def f_e(self):
        return self._f_e

    @property
    def d_f(self):
        return self._d_f

    @d_f.setter
    def d_f(self, value):
        self._d_f = value

    @property
    def d_e(self):
        return self._d_e

    def set_equation(self, dof_map, k_global, d_global, f_global, essential_global_dof_set):
        """Sets the FEM equation """

        # partition matrix
        if not isinstance(k_global, dok_matrix):
            raise TypeError("k_global must be a dok_matrix")

        N_essential = len(essential_global_dof_set)
        N_free = len(dof_map)-N_essential

        self._k_ee = scipy.sparse.dok_matrix( (N_essential, N_essential))
        self._k_ef = scipy.sparse.dok_matrix( (N_essential, N_free))
        self._k_fe = scipy.sparse.dok_matrix( (N_free, N_essential))
        self._k_ff = scipy.sparse.dok_matrix( (N_free, N_free))

        # partition k_global through calls to popitem
        # while k_global.getnnz() > 0:
        for key, value in k_global.items():
            # key, value = k_global.popitem()
            global_i, global_j = key

            if global_i < N_essential:
                if global_j < N_essential:
                    self._k_ee[ global_i, global_j] = value
                else:
                    self._k_ef[ global_i, global_j-N_essential] = value
            else:
                if global_j < N_essential:
                    self._k_fe[ global_i-N_essential, global_j] = value
                else:
                    self._k_ff[ global_i-N_essential, global_j-N_essential] = value

        # convert sparse matrix to data structures that are computationally efficient
        self._k_ee = self._k_ee.tocsr()
        self._k_fe = self._k_fe.tocsr()
        self._k_ef = self._k_ef.tocsr()
        self._k_ff = self._k_ff.tocsr()

        # partition d_global
        split_d_global = numpy.split(d_global, [N_essential]);
        self._d_e = split_d_global[0]
        self._d_f = split_d_global[1]

        # partition f_global
        split_f_global = numpy.split(f_global, [N_essential]);
        self._f_e = split_f_global[0]
        self._f_f = split_f_global[1]


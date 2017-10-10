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


from scipy.sparse import dok_matrix, coo_matrix
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg
import numpy
from barman import equations

class LinearStatic:
    """Performs a linear static analysis on a LinearElastic model"""


    class Results:
        """Stores the results of an analysis"""

        def __init__(self, model, equation, dof_order):
            self._model = model
            self._equation = equation
            self._dof_order = dof_order

        def get_equation(self):
            return self._equation

        def get_dof_order(self):
            return self._dof_order


    def __init__(self):
        pass


    def get_global_dof_map(self, model):
        """Returns a map with the GlobalDoF indices"""
        
        dof_order = dict()
        essential_global_dofs = set()

        #first register essential DoFs
        for pf in model.prescribed_displacements:
            for gdof,value in pf.get_values():
                if gdof not in essential_global_dofs:
                    essential_global_dofs.add(gdof)
                    dof_order[gdof] = len(dof_order)

        # then register all remaining global dofs
        for elem in model.elements:
            for gdof in elem.get_global_dofs():
                if gdof not in dof_order:
                    dof_order[gdof] = len(dof_order)

        return dof_order, essential_global_dofs


    def run(self, model):
        """Runs a linear static analysis on a linear elastic model"""

        # get list of GlobalDofs
        dof_map, essential_global_dofs = self.get_global_dof_map(model);

        # generate FEM equation
        k_global = self.generate_global_stiffness_matrix(model.elements, dof_map)
        f_global = self.generate_global_force_vector(model.prescribed_forces, dof_map)
        d_global = self.generate_global_dof_vector(model.prescribed_displacements, dof_map)


        #setup equation
        equation = equations.LinearStatic(dof_map, k_global, d_global, f_global, essential_global_dofs)

        #solve equation
        equation = self.solve_equation(equation)

        #output the result
        results = LinearStatic.Results(model, equation, dof_map)

        return results


    def generate_global_stiffness_matrix(self, elements, dof_order):
        """given a set of elements and a node ordering, generates a global stiffness matrix"""

        n_rows = n_columns = len(dof_order)
        k_global = dok_matrix( (n_rows, n_columns) )

        for elem in elements:
            k_elem = elem.get_global_stiffness_matrix()
            global_dofs = elem.get_global_dofs()

            # get indices
            indices = [dof_order[dof] for dof in global_dofs]

            for local_i, global_i in enumerate(indices):
                for local_j,global_j in enumerate(indices):
                    k_global[global_i,global_j] += k_elem[local_i,local_j]

        return k_global


    def generate_global_force_vector(self, prescribed_forces, dof_order):
        """given a set of prescribed forces and a node ordering, generates a global force vector"""

        n_rows = n_columns = len(dof_order)
        f_global = numpy.zeros(n_rows)


        for pf in prescribed_forces:
            f_elem = pf.value
            global_dofs = pf.global_dof

            global_i = dof_order[global_dofs]

            f_global[global_i] += f_elem

        return f_global


    def generate_global_dof_vector(self, prescribed_displacements, dof_order):
        """given a set of prescribed displacements and a node ordering, generates a global dof vector"""

        n_rows = n_columns = len(dof_order)
        d_global = numpy.zeros(n_rows)


        for pd in prescribed_displacements:
            d_elem = pd.value
            global_dofs = pd.global_dof

            global_i = dof_order[global_dofs]

            d_global[global_i] += d_elem

        return d_global


    def solve_equation(self, equation):
        """solves the equation"""

        #assembles the force vector
        if len(equation.d_e) > 0:
            f = equation.f_f - equation.k_fe.dot(equation.d_e)

            equation.d_f = scipy.sparse.linalg.spsolve(equation.k_ff, f)

        return equation

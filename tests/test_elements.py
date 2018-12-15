import unittest

from barman import materials, dofs, sections
from barman.elements import Bar2, EulerBernoulli


class CommonTests:

    def setUp(self):
        self.nodes = [ dofs.Node([0,0]), dofs.Node([2,0]) ]
        self.material = materials.LinearElastic('test', 100, 0.35);
        self.section = sections.Section(1, 1);


    def test_get_local_stiffness_matrix_expect_square_matrix(self):

        element = self.getElement()
        k = element.get_local_stiffness_matrix()

        k_rows, k_columns = k.shape

        self.assertEqual(k_rows, k_columns)


    def test_get_global_stiffness_matrix_expect_square_matrix(self):

        element = self.getElement()
        k = element.get_global_stiffness_matrix()

        k_rows, k_columns = k.shape

        self.assertEqual(k_rows, k_columns)


    def test_get_global_stiffness_matrix_expect_matrix_with_n_dof_rows(self):

        element = self.getElement()
        k = element.get_global_stiffness_matrix()

        k_rows, k_columns = k.shape
        n_dofs = len(element.get_global_dofs())

        self.assertEqual(k_rows, n_dofs)



class TestBar2Methods(CommonTests, unittest.TestCase):

    def getElement(self):
        return Bar2(self.nodes, self.section, self.material)


    def test_get_global_dofs_length(self):

        element = self.getElement()
        global_dofs = element.get_global_dofs()

        self.assertEqual(len(global_dofs), 4)


    def test_get_bar_length(self):

        element = self.getElement()
        bar_length = element.get_length()

        self.assertEqual(bar_length, 2)


    def test_get_transformation_matrix(self):

        element = self.getElement()

        T = element.get_transformation_matrix()



class TestEulerBernoulliMethods(CommonTests, unittest.TestCase):

    def getElement(self):
        return EulerBernoulli(self.nodes, self.section, self.material)


    def test_get_global_dofs_length(self):

        element = self.getElement()
        global_dofs = element.get_global_dofs()

        self.assertEqual(len(global_dofs), 6)


    def test_get_bar_length(self):

        element = self.getElement()
        bar_length = element.get_length()

        self.assertEqual(bar_length, 2)


if __name__ == '__main__':
    unittest.main()

import unittest

from barman import materials, dofs, sections
from barman.elements import Bar2, EulerBernoulli

class TestBar2Methods(unittest.TestCase):

    def setUp(self):
        self.nodes = [ dofs.Node([0,0]), dofs.Node([2,0]) ]
        self.material = materials.LinearElastic('test', 100, 0.35);
        self.section = sections.Section(1, 1);
        

    def test_get_global_dofs_length(self):
    
        element = Bar2(self.nodes, self.section, self.material)
        global_dofs = element.get_global_dofs()

        self.assertEqual(len(global_dofs), 4)


    def test_get_bar_length(self):
        element = Bar2(self.nodes, self.section, self.material)
        bar_length = element.get_length()

        self.assertEqual(bar_length, 2)
        

    def test_get_local_stiffness_matrix(self):
        element = Bar2(self.nodes, self.section, self.material)
        k = element.get_local_stiffness_matrix()


    def test_get_transformation_matrix(self):
        element = Bar2(self.nodes, self.section, self.material)
        T = element.get_transformation_matrix()


class TestEulerBernoulliMethods(unittest.TestCase):

    def setUp(self):
        self.nodes = [ dofs.Node([0,0]), dofs.Node([2,0]) ]
        self.material = materials.LinearElastic('test', 100, 0.35);
        self.section = sections.Section(1, 1);
        

    def test_get_global_dofs_length(self):
    
        element = EulerBernoulli(self.nodes, self.section, self.material)
        global_dofs = element.get_global_dofs()

        self.assertEqual(len(global_dofs), 6)


    def test_get_bar_length(self):
        element = EulerBernoulli(self.nodes, self.section, self.material)
        bar_length = element.get_length()

        self.assertEqual(bar_length, 2)
        

    def test_get_local_stiffness_matrix(self):
        element = EulerBernoulli(self.nodes, self.section, self.material)
        k = element.get_local_stiffness_matrix()
        


if __name__ == '__main__':
    unittest.main()

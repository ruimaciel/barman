import unittest

from barman import models
from barman import materials, dofs, sections
from barman.prescribed_displacements import PrescribedDisplacement
from barman.elements import Bar2, EulerBernoulli

class TestLinearElasticMethods(unittest.TestCase):

    def setUp(self):
        self.nodes = [ dofs.Node([0,0]), dofs.Node([1,0]), dofs.Node([1,1]) ]
        self.material = materials.LinearElastic('test', 100, 0.35);
        self.section = sections.Section(1, 1);
        

    def test_append_element(self):
        model = models.LinearStatic()

        elem = Bar2(self.nodes, self.section, self.material)

        model.append_element(elem)
        elem = model.elements

        self.assertEqual(len(elem), 1)


if __name__ == '__main__':
    unittest.main()

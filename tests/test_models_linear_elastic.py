import unittest

from barman import models
from barman.analysis import LinearStatic
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


    def test_get_global_dof_map(self):
        """ tests the generation of the GlobalDoF map"""

        model = models.LinearStatic()

        elem = Bar2([self.nodes[0], self.nodes[1]], self.section, self.material)

        model.append_element(elem)

        # now, let's set the beam as a singly-supported
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dx), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dy), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[1], dofs.Parameter.dy), 0))


        analysis = LinearStatic()

        global_dofs, essential_global_dofs = analysis.get_global_dof_map(model)
        
        self.assertEqual(len(global_dofs), 4)
    

    def test_generate_global_dof_vector(self):
        """ tests the generation of the GlobalDoF map"""

        model = models.LinearStatic()

        elem = Bar2([self.nodes[0], self.nodes[1]], self.section, self.material)

        model.append_element(elem)

        # now, let's set the beam as a singly-supported
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dx), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dy), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[1], dofs.Parameter.dy), 0))

        analysis = LinearStatic()
        global_dof_map = analysis.get_global_dof_map(model);
        global_dof_map, essential_global_dofs = analysis.get_global_dof_map(model)

        global_dofs = analysis.generate_global_dof_vector(model.prescribed_displacements, global_dof_map)
        
        self.assertEqual(len(global_dofs), 4)
    

    def test_run(self):
        model = models.LinearStatic()
        model.append_element( Bar2([self.nodes[0], self.nodes[1]], self.section, self.material) )
        model.append_element( Bar2([self.nodes[1], self.nodes[2]], self.section, self.material) )
        model.append_element( Bar2([self.nodes[0], self.nodes[2]], self.section, self.material) )

        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dx), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[0], dofs.Parameter.dy), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[1], dofs.Parameter.dx), 0))
        model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(self.nodes[1], dofs.Parameter.dy), 0))

        analysis = LinearStatic()
        result = analysis.run(model)


if __name__ == '__main__':
    unittest.main()

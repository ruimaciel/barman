import unittest

from barman import dofs
from math import pi
import numpy

class TestCoordinateSystemMethods(unittest.TestCase):

    def test_get_transformation(self):
        coordinate_system = dofs.CoordinateSystem(pi/2)
        T = coordinate_system.get_transformation()

        u = numpy.array([1,0,0])

        v = T.dot(u)

        self.assertAlmostEqual(max(v - [0, 1, 0]), 0 )


class TestNodeMethods(unittest.TestCase):

    def test_get_position(self):
        position = [0, 0]

        node = dofs.Node(position)

        self.assertEqual(position, node.position)


if __name__ == '__main__':
    unittest.main()

import unittest
from networkx import simple_cycles
from rotorgraph import RotorGraph
from rotor_config import RotorConfig
from vector import Vector
from particle_config import ParticleConfig


class TestRotorConfig(unittest.TestCase):

    def test_cyclepush(self):
        configuration = {1: (1, 2, 0), 2: (2, 1, 0), 3: (3, 4, 0), 4: (4, 3, 0)}
        rc = RotorConfig(configuration)
        
        g = rc.to_graph()
        expected_len = len(list(simple_cycles(g)))
        calculated_len = len(rc.find_cycles())
        self.assertEqual(expected_len, calculated_len)

    def test_DF(self):
        pass
        

if __name__ == '__main__':
    unittest.main()


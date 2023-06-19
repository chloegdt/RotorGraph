import unittest
from networkx import simple_cycles
from rotorgraph import RotorGraph
from rotorconfig import RotorConfig
from vector import Vector
from particleconfig import ParticleConfig


class TestRotorConfig(unittest.TestCase):

    def test_len_cycles(self):
        configuration = {1: (1, 2, 0), 2: (2, 1, 0), 3: (3, 4, 0), 4: (4, 3, 0)}
        rc = RotorConfig(configuration)
        
        g = rc.to_graph()
        expected_len = len(list(simple_cycles(g)))
        calculated_len = len(rc.find_cycles())
        self.assertEqual(expected_len, calculated_len)

    def test_edges(self):
        for i in range(2,9):
            G = RotorGraph.simple_path(i)
            rho = RotorConfig(G)
            cmp_r = 0
            cmp_l = 0
            for edge in rho.values():
                if edge[1] > edge[0]: 
                    cmp_r += 1
                else:
                    cmp_l += 1


            while cycles := rho.find_cycles(G.sinks):
                for cycle in cycles:
                    rho.cycle_push(G, cycle)
                    res_r = 0
                    res_l = 0
                
                    for edge in rho.values():
                        if edge[1] > edge[0]: 
                            res_r += 1
                        else:
                            res_l += 1

                self.assertEqual(res_r, cmp_r)
                self.assertEqual(res_l, cmp_l)


if __name__ == '__main__':
    unittest.main()


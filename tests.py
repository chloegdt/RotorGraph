import unittest
from networkx import simple_cycles, strongly_connected_components
from rotorgraph import RotorGraph
from rotorconfig import RotorConfig
from vector import Vector
from particleconfig import ParticleConfig
from random import randint
from numpy import array, linalg


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



class TestRotorGraph(unittest.TestCase):

    def test_classes(self):
        """"""
        G = RotorGraph.random_graph()
        cp = list(strongly_connected_components(G))
        #self.assertTrue((len(cp) == 2) and ({G.number_of_nodes()-1} in cp))

        mx = G.reduced_laplacian_matrix()
        new_mx = [list(line.values()) for line in mx.values()]
        n_array = array(new_mx)
        det = linalg.det(n_array)

        ac = G.enum_acyclic_configurations()
        self.assertEqual(len(ac),round(det))

class TestVector(unittest.TestCase):

    def test_dic_methods(self):
        """doc"""

        dic = {randint(0, 100):randint(0, 100) for _ in range(randint(1, 20)) }
        v = Vector(dic)
            
        v[200] = 12
        dic[200] = 12
        self.assertEqual(v[200], dic[200])

        del v[200]
        #del dic[200]

        self.assertEqual(dic.keys(), v.keys())
        self.assertEqual(list(dic.values()), list(v.values()))
        self.assertEqual(dic.items(), v.items())


    def test_comparisons(self):
        """doc"""

        for _ in range(50):

            n = randint(2,20)
            dic1 = {i:randint(0, 20) for i in range(n)}
            v1 = Vector(dic1)
            dic2 = {i: randint(21, 40) for i in range(n)}
            v2 = Vector(dic2)
            dic3 = {randint(0, 100): (randint(0, 20) if i < n//2 else randint(21,40)) for i in range(n)} 
            v3 = Vector(dic3)
            

            # tests between 2 vectors
            self.assertTrue(v1 < v2)
            self.assertTrue(v2 > v1)
            self.assertTrue(v1 <= v2)
            self.assertTrue(v2 >= v1)
            self.assertFalse(v1 == v2)
            self.assertTrue(v1 != v2)

            # tests
            self.assertFalse(v1 > randint(21, 40))
            self.assertTrue(v1 < randint(21, 40))

            self.assertTrue(v2 > randint(0, 20))
            self.assertTrue(v2 >= randint(0, 21))




if __name__ == '__main__':
    unittest.main()


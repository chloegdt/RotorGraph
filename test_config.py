import unittest
from networkx import strongly_connected_components
from rotorgraph import RotorGraph
from vector import Vector
from rotorconfig import RotorConfig
from random import randint
from numpy import array, linalg

class TestRotorGraph(unittest.TestCase):

    def test_classes(self):
        """"""
        G = RotorGraph.random_graph()
        print(G)
        print(G.nodes)
        for node in G.rotor_order:
            print(node, G.rotor_order[node])
        cp = list(strongly_connected_components(G))
        self.assertTrue((len(cp) == 2) and ({G.number_of_nodes()-1} in cp))

        mx = G.reduced_laplacian_matrix()
        new_mx = [list(line.values()) for line in mx.values()]
        n_array = array(new_mx)
        print(n_array)
        det = linalg.det(n_array)

        ac = G.enum_acyclic_configurations()
        print(len(ac))
        print(round(det))
        self.assertEqual(len(ac),round(det))


if __name__ == "__main__":
    unittest.main()

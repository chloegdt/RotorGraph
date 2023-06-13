import networkx as nx
from vector import Vector
from rotor_config import RotorConfig
from rotorgraph import RotorGraph

def main():
    G = RotorGraph.simple_path()
    rho = RotorConfig(G)
    print(rho)
    a = (1,0,0)
    v = Vector(rho) - a + G.turn(a)
    print(v)



if __name__ == "__main__":
    main()

import networkx as nx
from vector import Vector
from rotor_config import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent
from particle_config import ParticleConfig

def main():
    #n = 5
    #G = RotorGraph.grid(n,n)
    #for i in range(n): G.set_sink(i, i+(n*(n-1)), i*n, i*n+n-1)

    G = RotorGraph.simple_path()
    sigma = ParticleConfig(G)
    ac = G.enum_acyclic_configurations()
    #for config in ac: print(config)
    #print(len(ac))

    rec = G.recurrent_and_acyclic(ac)
    for rec, acy in rec:
        display_path(rec, sigma)
        display_path(acy, sigma)
        for conig in all_config_from_recurrent(G, rec):
            display_path(conig, sigma)
        print()

if __name__ == "__main__":
    main()

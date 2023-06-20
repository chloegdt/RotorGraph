import networkx as nx
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig


def main():
    sigma = ParticleConfig()
    G = RotorGraph.simple_path()
    rho = RotorConfig(G)
    display_path(rho)
    G.route_one_particle(2, rho)
    display_path(rho)

    #ac = G.enum_acyclic_configurations()
    #for config in ac: print(config)
    #print(len(ac))

    #rec = G.recurrent_and_acyclic(ac)
    #for rec, acy in rec:
        #for conig in all_config_from_recurrent(G, rec): display_path(conig)
        #print()

if __name__ == "__main__":
    main()

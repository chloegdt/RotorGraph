import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig



def main():
    
    for n in range(2, 6):
        for x in range(1, 6):
            for y in range(1, 6):
                res = max_steps(n, x, y)
                print("n:", n, "| x:", x, "| y:", y, "| steps:", res[0][0])
        print()

def max_steps(n:int=5, x:int=1, y:int=1) -> (RotorConfig, Node, int):
    """
    doc
    """
    nb_max = [(0, None, None)]
    G = RotorGraph.simple_path(n, x, y)
    for config in G.enum_configurations():
        for node in set(G.nodes)-set(G.sinks):
            rc, nb_steps = G.route_one_particle(node, config)
            if nb_steps > nb_max[0][0]:
                nb_max = [(nb_steps, node, config)]
            elif nb_steps == nb_max[0][0]:
                nb_max.append((nb_steps, node, config))

    return nb_max


if __name__ == "__main__":
    main()

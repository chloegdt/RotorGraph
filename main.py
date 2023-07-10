import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig
from matrices import Matrix

def simple_path_graph():
    G = RotorGraph.simple_path(n=5, x=1, y=1)
    rho = RotorConfig(G)
    G.check_rotor_config(rho)
    sigma = ParticleConfig(G)
    sigma.set_all_particles(3)

    display_path(rho, sigma)

    sigma, rho, info = G.legal_routing(sigma, rho)
    display_path(rho, sigma)

    # sigma.set_particles(3, -4)
    sigma[3] = -4
    display_path(rho, sigma)

    sigma, rho, info = G.complete_routing(sigma, rho)
    print(info)
    display_path(rho, sigma)




def laplacian_matrices():
    G = RotorGraph.simple_path()
    L = G.laplacian_matrix()
    rL = G.reduced_laplacian_matrix()
    print(L)
    print(rL)


def smith_normal_form():
    G = RotorGraph.simple_path()
    matrix = G.reduced_laplacian_matrix()
    print(matrix)
    prob = matrix.snf_problem()
    print(prob.J)
    print(prob.S)
    print(prob.T)

def acyclic_recurrents():
    G = RotorGraph.grid(3, 3, "borders")

    acy = G.enum_acyclic_configurations()
    for config in acy:
        display_grid(config, 3, 3)
        print("###########################")
    print("det =", G.reduced_laplacian_matrix().determinant())
    print("nb of acyclic =", len(acy))

    rec = G.recurrent_from_acyclic(acy)

    rec_acy = G.recurrent_and_acyclic(acy)


if __name__ == "__main__":
    acyclic_recurrents()


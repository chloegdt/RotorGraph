import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig
from matrices import Matrix

def particle_configuration():
    G = RotorGraph.simple_path()
    
    s1 = ParticleConfig(G)
    s1.set_all_particles(5)

    print("s1:", s1)
    s1 *= 2
    print("s1:", s1)

    s2 = ParticleConfig()
    s2[2] = 12
    print("s2:", s2)

    s3 = s1 + s2
    print("s3=s1+s2: ", s3)

    print("s1:", s1)
    print("s2:", s2)

    print("s2 + 2:", s2 + 2)

def rotor_configuration():
    G = RotorGraph.simple_path()
    rho = RotorConfig(G)
    display_path(rho)

    edge = (1, 0, 0)

    rho[1] = edge
    display_path(rho)

    vec = Vector(rho)
    vec = vec - edge + G.turn(edge)

    rho2 = RotorConfig(vec)

    display_path(rho2)


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
    print(prob.S * prob.A * prob.T)

def acyclic_recurrents():
    G = RotorGraph.grid(3, 3, "corner")

    acy = G.enum_acyclic_configurations()
    for config in acy:
        display_grid(config, 3, 3)
        print("###########################")
    print("det =", G.reduced_laplacian_matrix().determinant())
    print("nb of acyclic =", len(acy))

    rec = G.recurrent_from_acyclic(acy)

    rec_acy = G.recurrent_and_acyclic(acy)
    for tupl in rec_acy: print(tupl)


if __name__ == "__main__":
    #acyclic_recurrents()
    #particle_configuration()
    #rotor_configuration()
    #simple_path_graph()
    #smith_normal_form()
    G = RotorGraph.simple_path()
    rho = RotorConfig(G)
    _, info = G.route_one_particle(2, rho)
    for rho, sigma in info.configuration_history:
        display_path(rho, sigma)


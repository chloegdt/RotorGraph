import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig

def equal(n, x):
    if not n%2: return (x*n*n + n)//2 # even
    else: return (x*n*n - x + n + 1)//2 # odd

def different(n, x):
    return -2*x + n + 2*n*x

def f(n, x, y):
    if x == y: return equal(n, x)
    else: return different(n, min(x,y))


def expected_max_steps(n:int, x:int, y:int):
    if x == y: return -2*x + n + 2*n*x
    elif n%2: return (x*n*n + n - x + 1) // 2
    else: return (x*n*n + n) // 2


def max_steps(n:int=5, x:int=1, y:int=1) -> (RotorConfig, Node, int):
    """
    doc
    """
    nb_max = [(0, None, None)]
    G = RotorGraph.simple_path(n, x, y)
    nro = {1:[(1,2,1), (1,0,0), (1,2,0), (1,0,1), (1,2,2)], 2:[(2,1,0), (2,1,1), (2,3,2), (2,3,1),(2,3,0)], 3:[(3,2,1), (3,4,0),(3,4,2), (3,2,0), (3,4,1)]}
    #G.set_rotor_order(nro)
    rec = G.recurrent_from_acyclic(G.enum_acyclic_configurations())
    for config in G.enum_configurations():
        for node in set(G.nodes)-set(G.sinks):
            rc, nb_steps = G.route_one_particle(node, config)
            if nb_steps > nb_max[0][0]:
                nb_max = [(nb_steps, node, config)]
            elif nb_steps == nb_max[0][0]:
                nb_max.append((nb_steps, node, config))
    return nb_max


def max_config(n, x, y):
    rc = dict()
    if x > y:
        node = n
        for i in range(1, n+1):
            if i == node:
                rc[i] = (i, i-1, 0)
            elif i != node:
                rc[i] = (i, i+1, 0)
    elif x < y:
        node = 1
        for i in range(1, n+1):
            if i == node:
                rc[i] = (i, i+1, 0)
            elif i != node:
                rc[i] = (i, i-1, 0)
    elif x == y:
        node = (n+1)//2
        for i in range(1, n+1):
            if i <= node:
                rc[i] = (i, i+1, 0)
            elif i > node:
                rc[i] = (i, i-1, 0)

    return RotorConfig(rc), node

def better_max_steps(n:int=5, x:int=1, y:int=1) -> (RotorConfig, Node, int):
    """doc"""
    G = RotorGraph.simple_path(n, x, y)
    config, node = max_config(n,x,y)
    rc, nb_steps = G.route_one_particle(node, config)
    return nb_steps

def testing_the_test():
    for n in range(1, 20):
        print(f"### n = {n} ###")
        print("x y steps")
        for x in range(1, 20):
            for y in range(x, x+4):
                res = better_max_steps(n, x, y)
                print(x, y, res)
        print()

def testing():
    n, x, y = 4, 3, 3
    res = max_steps(n,x,y)
    print(res)
    for nb_steps, node, config in res:
        for n, edge in config.items():
            if n == node: print('[', end='')
            if edge[0] < edge[1]: print('>', end='')
            if edge[0] > edge[1]: print('<', end='')
            print(edge[2], end='')
            if n == node: print(']', end='')
            print(' ',end='')
        print()





if __name__ == "__main__":
    testing_the_test()

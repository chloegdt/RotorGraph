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
    if x != y: return -2*x + n + 2*n*x
    elif n%2: return (x*n*n + n - x + 1) // 2
    else: return (x*n*n + n) // 2


def max_steps(n:int=5, x:int=1, y:int=1) -> (RotorConfig, Node, int):
    """
    doc
    """
    nb_steps = 0
    configs = [(None, None)]
    G = RotorGraph.simple_path(n, x, y)
    
    #nro = {1:[(1,2,1), (1,0,0), (1,2,0), (1,0,1), (1,2,2)], 2:[(2,1,0), (2,1,1), (2,3,2), (2,3,1),(2,3,0)], 3:[(3,2,1), (3,4,0),(3,4,2), (3,2,0), (3,4,1)]}
    #G.set_rotor_order(nro)
    #rec = G.recurrent_from_acyclic(G.enum_acyclic_configurations())
    
    for config in G.enum_configurations():
        for node in set(G.nodes)-set(G.sinks):
            rc, n = G.route_one_particle(node, config)
            if n > nb_steps:
                configs = [(node, config)]
                nb_steps = n
            elif n == nb_steps:
                configs.append((node, config))
    return nb_steps, configs


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
    for n in range(1, 30):
        print(f"### n = {n} ###")
        print(" x  y steps expected")
        for x in range(1, 25):
            for y in range(x, x+5):
                res = better_max_steps(n, x, y)
                res = ' '*(5-len(str(res)))+str(res)

                e = expected_max_steps(n,x,y)
                e = ' '*(8-len(str(e)))+str(e)

                sx = ' '*(2-len(str(x)))+str(x)
                sy = ' '*(2-len(str(y)))+str(y)
                print(sx, sy, res, e)
        print()

def testing():
    n, x, y = 4, 3, 3
    nb_steps, configs = max_steps(n,x,y)
    G = RotorGraph.simple_path(n, x, y)
    recurrents = G.recurrent_from_acyclic(G.enum_acyclic_configurations())

    print("nombre d'etapes maximal: ", nb_steps)
    for node, config in configs:
        display_config(config)
        print()

        for recurrent in recurrents:
            if config in all_config_from_recurrent(G, recurrent):
                display_config(recurrent)

        if config in recurrents: print(" rec")
        else: print()
    test_recurrents(n,x,y)

def test_recurrents(n,x,y):
    G = RotorGraph.simple_path(n, x, y)
    recurrents = G.recurrent_from_acyclic(G.enum_acyclic_configurations())
    for config in recurrents:
        display_config(config)
        nb_steps = 0
        for node in set(G.nodes)-set(G.sinks):
            rc, n = G.route_one_particle(node, config)
            if nb_steps < n: nb_steps = n
        print("", nb_steps)


def display_config(config, node=None):
    for n, edge in config.items():
        if node != None and n == node: print('[', end='')
        if edge[0] < edge[1]: print('>', end='')
        if edge[0] > edge[1]: print('<', end='')
        print(edge[2], end='')
        if node != None and n == node: print(']', end='')
        print(' ',end='')






if __name__ == "__main__":
    #testing_the_test()
    #testing()
    G = RotorGraph.simple_path()
    rec = G.recurrent_and_acyclic(G.enum_acyclic_configurations())
    for rec, acy in rec:
        for config in all_config_from_recurrent(G, rec): display_path(config)
        print()
